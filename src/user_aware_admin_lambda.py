import json
import boto3
import uuid
import base64
from datetime import datetime
from botocore.exceptions import ClientError
import jwt
from jwt.exceptions import InvalidTokenError
import re

# AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
cognito_client = boto3.client('cognito-idp')
cloudfront_client = boto3.client('cloudfront')

# Configuration
BUCKET_NAME = 'dataiesb'
REPORTS_TABLE = 'dataiesb-reports'
COGNITO_USER_POOL_ID = 'us-east-1_QvLQs82bE'
COGNITO_REGION = 'us-east-1'
CLOUDFRONT_DISTRIBUTION_ID = 'E371T2F886B5KI'

# DynamoDB table
table = dynamodb.Table(REPORTS_TABLE)

def lambda_handler(event, context):
    try:
        # CORS headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*'
        }
        
        # Handle OPTIONS request
        if event['httpMethod'] == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Get user email from token
        user_email = get_user_email_from_token(event)
        if not user_email:
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'message': 'Unauthorized - Invalid or missing token'})
            }
        
        # Validate IESB email domain
        if not user_email.endswith('@iesb.edu.br'):
            return {
                'statusCode': 403,
                'headers': headers,
                'body': json.dumps({'message': 'Access denied - Only @iesb.edu.br emails allowed'})
            }
        
        method = event['httpMethod']
        path = event['path']
        
        # Handle GET /reports - list user's reports only
        if method == 'GET' and path.endswith('/reports'):
            return get_user_reports(user_email, headers)
        
        # Handle GET /reports/{id}/download - download user's report file
        if method == 'GET' and '/reports/' in path and path.endswith('/download'):
            report_id = path.split('/reports/')[-1].replace('/download', '')
            return download_user_report(user_email, report_id, headers)
        
        # Handle POST /reports - create report for user
        if method == 'POST' and path.endswith('/reports'):
            return create_user_report(event, user_email, headers)
        
        # Handle PUT /reports/{id} - update user's report
        if method == 'PUT' and '/reports/' in path:
            report_id = path.split('/reports/')[-1]
            return update_user_report(event, user_email, report_id, headers)
        
        # Handle DELETE /reports/{id} - delete user's report
        if method == 'DELETE' and '/reports/' in path:
            report_id = path.split('/reports/')[-1]
            return delete_user_report(user_email, report_id, headers)
        
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'message': 'Not found'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps({'message': f'Internal server error: {str(e)}'})
        }

def get_user_email_from_token(event):
    """Extract user email from Authorization header"""
    try:
        # Get Authorization header
        auth_header = event.get('headers', {}).get('Authorization') or event.get('headers', {}).get('authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.replace('Bearer ', '')
        
        # Decode JWT token (without verification for now - in production, verify signature)
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        # Get email from token
        email = decoded.get('email') or decoded.get('username')
        return email
        
    except Exception as e:
        print(f"Error extracting email from token: {e}")
        return None

def get_next_report_id():
    """Get the next incremental report ID"""
    try:
        # Scan table to find the highest report_id
        response = table.scan(
            ProjectionExpression='report_id'
        )
        
        max_id = 0
        for item in response['Items']:
            try:
                # Try to convert report_id to integer
                current_id = int(item['report_id'])
                if current_id > max_id:
                    max_id = current_id
            except (ValueError, TypeError):
                # Skip non-numeric IDs (like UUIDs from previous tests)
                continue
        
        return str(max_id + 1)
        
    except Exception as e:
        print(f"Error getting next report ID: {e}")
        # Fallback to timestamp-based ID if scan fails
        return str(int(datetime.utcnow().timestamp()))

def parse_multipart_form_data(event):
    """Parse multipart form data from API Gateway event"""
    try:
        content_type = event.get('headers', {}).get('content-type', '')
        if 'multipart/form-data' not in content_type:
            return None, None
        
        # Extract boundary
        boundary_match = re.search(r'boundary=([^;]+)', content_type)
        if not boundary_match:
            return None, None
        
        boundary = boundary_match.group(1)
        
        # Decode body
        body = event.get('body', '')
        if event.get('isBase64Encoded', False):
            body = base64.b64decode(body).decode('utf-8')
        
        # Parse form data
        form_data = {}
        file_data = None
        
        # Split by boundary
        parts = body.split(f'--{boundary}')
        
        for part in parts:
            if 'Content-Disposition: form-data' in part:
                # Extract field name
                name_match = re.search(r'name="([^"]+)"', part)
                if not name_match:
                    continue
                
                field_name = name_match.group(1)
                
                # Check if it's a file
                if 'filename=' in part:
                    filename_match = re.search(r'filename="([^"]+)"', part)
                    if filename_match:
                        filename = filename_match.group(1)
                        # Extract file content (after double newline)
                        content_start = part.find('\r\n\r\n')
                        if content_start != -1:
                            file_content = part[content_start + 4:].rstrip('\r\n')
                            file_data = {
                                'filename': filename,
                                'content': file_content,
                                'field_name': field_name
                            }
                else:
                    # Regular form field
                    content_start = part.find('\r\n\r\n')
                    if content_start != -1:
                        field_value = part[content_start + 4:].rstrip('\r\n')
                        form_data[field_name] = field_value
        
        return form_data, file_data
        
    except Exception as e:
        print(f"Error parsing multipart data: {e}")
        return None, None

def get_user_reports(user_email, headers):
    """Get all reports for a specific user"""
    try:
        # Query reports by user email using GSI
        response = table.query(
            IndexName='user-email-index',
            KeyConditionExpression='user_email = :email',
            ExpressionAttributeValues={':email': user_email}
        )
        
        # Format response as dict with report_id as key
        reports = {}
        for item in response['Items']:
            if not item.get('deletado', False):  # Only include non-deleted reports
                reports[item['report_id']] = {
                    'titulo': item['titulo'],
                    'autor': item['autor'],
                    'descricao': item['descricao'],
                    'created_at': item['created_at'],
                    'updated_at': item['updated_at']
                }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(reports)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Error fetching reports: {str(e)}'})
        }

def download_user_report(user_email, report_id, headers):
    """Download a report file if it belongs to the user"""
    try:
        # Check if report belongs to user
        response = table.get_item(Key={'report_id': report_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': 'Report not found'})
            }
        
        report = response['Item']
        if report['user_email'] != user_email:
            return {
                'statusCode': 403,
                'headers': headers,
                'body': json.dumps({'message': 'Access denied - Report belongs to another user'})
            }
        
        # Get file from S3
        s3_key = f'reports/{report_id}/main.py'
        try:
            s3_response = s3_client.get_object(Bucket=BUCKET_NAME, Key=s3_key)
            file_content = s3_response['Body'].read()
            
            # Return file as base64 encoded response
            return {
                'statusCode': 200,
                'headers': {
                    **headers,
                    'Content-Type': 'text/x-python',
                    'Content-Disposition': f'attachment; filename="report_{report_id}.py"'
                },
                'body': base64.b64encode(file_content).decode('utf-8'),
                'isBase64Encoded': True
            }
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'Report file not found in storage'})
                }
            else:
                raise e
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Error downloading report: {str(e)}'})
        }

def create_user_report(event, user_email, headers):
    """Create a new report for the user with file upload"""
    try:
        # Parse multipart form data
        form_data, file_data = parse_multipart_form_data(event)
        
        if not form_data or not file_data:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Invalid form data or missing file'})
            }
        
        # Generate incremental report ID
        report_id = get_next_report_id()
        timestamp = datetime.utcnow().isoformat()
        
        # Upload file to S3
        s3_key = f'reports/{report_id}/main.py'
        try:
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=s3_key,
                Body=file_data['content'],
                ContentType='text/x-python'
            )
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'message': f'Error uploading file to S3: {str(e)}'})
            }
        
        # Create DynamoDB entry
        table.put_item(
            Item={
                'report_id': report_id,
                'user_email': user_email,
                'titulo': form_data.get('titulo', 'Untitled Report'),
                'autor': form_data.get('autor', user_email.split('@')[0]),
                'descricao': form_data.get('descricao', 'No description'),
                'created_at': timestamp,
                'updated_at': timestamp,
                'deletado': False,
                'id_s3': f'reports/{report_id}/'
            }
        )
        
        # Invalidate CloudFront cache for the report
        try:
            invalidate_cloudfront_cache([f'/reports/{report_id}/*'])
        except Exception as e:
            print(f"CloudFront invalidation failed: {e}")
            # Don't fail the request if CloudFront invalidation fails
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Report created successfully',
                'report_id': report_id,
                's3_key': s3_key
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Error creating report: {str(e)}'})
        }

def update_user_report(event, user_email, report_id, headers):
    """Update a report if it belongs to the user"""
    try:
        # Check if report belongs to user
        response = table.get_item(Key={'report_id': report_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': 'Report not found'})
            }
        
        report = response['Item']
        if report['user_email'] != user_email:
            return {
                'statusCode': 403,
                'headers': headers,
                'body': json.dumps({'message': 'Access denied - Report belongs to another user'})
            }
        
        # Parse form data for updates
        form_data, file_data = parse_multipart_form_data(event)
        
        # Update report metadata
        timestamp = datetime.utcnow().isoformat()
        update_expression = 'SET updated_at = :timestamp'
        expression_values = {':timestamp': timestamp}
        
        if form_data:
            if 'titulo' in form_data:
                update_expression += ', titulo = :titulo'
                expression_values[':titulo'] = form_data['titulo']
            if 'autor' in form_data:
                update_expression += ', autor = :autor'
                expression_values[':autor'] = form_data['autor']
            if 'descricao' in form_data:
                update_expression += ', descricao = :descricao'
                expression_values[':descricao'] = form_data['descricao']
        
        # Update file if provided
        if file_data:
            s3_key = f'reports/{report_id}/main.py'
            try:
                s3_client.put_object(
                    Bucket=BUCKET_NAME,
                    Key=s3_key,
                    Body=file_data['content'],
                    ContentType='text/x-python'
                )
                
                # Invalidate CloudFront cache
                invalidate_cloudfront_cache([f'/reports/{report_id}/*'])
                
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({'message': f'Error updating file: {str(e)}'})
                }
        
        # Update DynamoDB
        table.update_item(
            Key={'report_id': report_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Report updated successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Error updating report: {str(e)}'})
        }

def delete_user_report(user_email, report_id, headers):
    """Soft delete a report if it belongs to the user"""
    try:
        # Check if report belongs to user
        response = table.get_item(Key={'report_id': report_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': 'Report not found'})
            }
        
        report = response['Item']
        if report['user_email'] != user_email:
            return {
                'statusCode': 403,
                'headers': headers,
                'body': json.dumps({'message': 'Access denied - Report belongs to another user'})
            }
        
        # Soft delete report
        timestamp = datetime.utcnow().isoformat()
        table.update_item(
            Key={'report_id': report_id},
            UpdateExpression='SET deletado = :deleted, updated_at = :timestamp',
            ExpressionAttributeValues={
                ':deleted': True,
                ':timestamp': timestamp
            }
        )
        
        # Invalidate CloudFront cache
        try:
            invalidate_cloudfront_cache([f'/reports/{report_id}/*'])
        except Exception as e:
            print(f"CloudFront invalidation failed: {e}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Report deleted successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Error deleting report: {str(e)}'})
        }

def invalidate_cloudfront_cache(paths):
    """Invalidate CloudFront cache for specific paths"""
    try:
        caller_reference = f"lambda-invalidation-{int(datetime.utcnow().timestamp())}"
        
        response = cloudfront_client.create_invalidation(
            DistributionId=CLOUDFRONT_DISTRIBUTION_ID,
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(paths),
                    'Items': paths
                },
                'CallerReference': caller_reference
            }
        )
        
        print(f"CloudFront invalidation created: {response['Invalidation']['Id']}")
        return response
        
    except Exception as e:
        print(f"Error creating CloudFront invalidation: {e}")
        raise e
