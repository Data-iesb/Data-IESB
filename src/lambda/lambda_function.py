import json
import boto3
import base64
from datetime import datetime
import os

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Correct bucket for reports
REPORTS_BUCKET = 'dataiesb-reports'
REPORTS_TABLE = os.environ.get('REPORTS_TABLE', 'dataiesb-reports')

def lambda_handler(event, context):
    try:
        # Handle CORS preflight
        if event['httpMethod'] == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
                }
            }
        
        # Get user info from JWT token
        user_email = get_user_from_token(event.get('headers', {}).get('Authorization', ''))
        if not user_email:
            return error_response('Unauthorized', 401)
        
        method = event['httpMethod']
        path = event.get('path', '')
        
        if method == 'POST' and '/reports' in path:
            return create_report(event, user_email)
        elif method == 'GET' and '/reports' in path:
            if '/download' in path:
                return download_report(event, user_email)
            else:
                return list_reports(user_email)
        elif method == 'DELETE' and '/reports' in path:
            return soft_delete_report(event, user_email)
        elif method == 'PUT' and '/reports' in path and '/restore' in path:
            return restore_report(event, user_email)
        else:
            return error_response('Method not allowed', 405)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return error_response(f'Internal server error: {str(e)}', 500)

def get_next_report_id():
    """Generate the next incremental report ID"""
    try:
        table = dynamodb.Table(REPORTS_TABLE)
        
        # Scan table to find the highest existing report ID
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
                # Skip non-numeric IDs
                continue
        
        # Return next incremental ID
        return str(max_id + 1)
        
    except Exception as e:
        print(f"Error getting next report ID: {str(e)}")
        # Fallback to timestamp-based ID if there's an error
        return str(int(datetime.utcnow().timestamp()))

def get_user_from_token(auth_header):
    """Extract user email from JWT token"""
    try:
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        # Decode JWT payload (simplified - in production use proper JWT validation)
        payload = json.loads(base64.b64decode(token.split('.')[1] + '=='))
        return payload.get('email') or payload.get('username')
    except:
        return None

def create_report(event, user_email):
    """Create a new report and upload Python file to S3"""
    try:
        # Parse multipart form data
        content_type = event.get('headers', {}).get('content-type', '')
        if 'multipart/form-data' not in content_type:
            return error_response('Content-Type must be multipart/form-data', 400)
        
        body = base64.b64decode(event['body'])
        form_data = parse_multipart_form_data(body, content_type)
        
        # Validate required fields
        required_fields = ['titulo', 'autor', 'descricao', 'main']
        for field in required_fields:
            if field not in form_data:
                return error_response(f'Missing required field: {field}', 400)
        
        # Generate incremental ID for the report
        report_id = get_next_report_id()
        timestamp = datetime.utcnow().isoformat()
        
        # Upload Python file to correct S3 bucket (dataiesb-reports)
        file_key = f"{report_id}/main.py"
        
        s3_client.put_object(
            Bucket=REPORTS_BUCKET,
            Key=file_key,
            Body=form_data['main']['content'],
            ContentType='text/x-python',
            Metadata={
                'user': user_email,
                'report_id': report_id,
                'original_filename': form_data['main']['filename']
            }
        )
        
        # Save report metadata to DynamoDB
        table = dynamodb.Table(REPORTS_TABLE)
        table.put_item(
            Item={
                'report_id': report_id,
                'user_email': user_email,
                'titulo': form_data['titulo'],
                'autor': form_data['autor'],
                'descricao': form_data['descricao'],
                's3_key': file_key,
                'created_at': timestamp,
                'updated_at': timestamp,
                'is_deleted': False,  # Soft delete flag
                'deleted_at': None
            }
        )
        
        return success_response({
            'message': 'Report created successfully',
            'report_id': report_id,
            's3_bucket': REPORTS_BUCKET,
            's3_key': file_key
        })
        
    except Exception as e:
        print(f"Error creating report: {str(e)}")
        return error_response(f'Error creating report: {str(e)}', 500)

def list_reports(user_email):
    """List all non-deleted reports for the user"""
    try:
        table = dynamodb.Table(REPORTS_TABLE)
        
        response = table.scan(
            FilterExpression='user_email = :user_email AND is_deleted = :is_deleted',
            ExpressionAttributeValues={
                ':user_email': user_email,
                ':is_deleted': False
            }
        )
        
        reports = {}
        for item in response['Items']:
            reports[item['report_id']] = {
                'titulo': item['titulo'],
                'autor': item['autor'],
                'descricao': item['descricao'],
                'created_at': item['created_at'],
                'updated_at': item['updated_at']
            }
        
        return success_response(reports)
        
    except Exception as e:
        print(f"Error listing reports: {str(e)}")
        return error_response(f'Error listing reports: {str(e)}', 500)

def soft_delete_report(event, user_email):
    """Soft delete a report (mark as deleted instead of actually deleting)"""
    try:
        # Extract report_id from path
        path_parts = event['path'].split('/')
        report_id = path_parts[-1]
        
        table = dynamodb.Table(REPORTS_TABLE)
        
        # Check if report exists and belongs to user
        response = table.get_item(
            Key={'report_id': report_id}
        )
        
        if 'Item' not in response:
            return error_response('Report not found', 404)
        
        report = response['Item']
        if report['user_email'] != user_email:
            return error_response('Unauthorized to delete this report', 403)
        
        if report.get('is_deleted', False):
            return error_response('Report already deleted', 400)
        
        # Soft delete - mark as deleted
        table.update_item(
            Key={'report_id': report_id},
            UpdateExpression='SET is_deleted = :deleted, deleted_at = :deleted_at, updated_at = :updated_at',
            ExpressionAttributeValues={
                ':deleted': True,
                ':deleted_at': datetime.utcnow().isoformat(),
                ':updated_at': datetime.utcnow().isoformat()
            }
        )
        
        return success_response({'message': 'Report deleted successfully'})
        
    except Exception as e:
        print(f"Error deleting report: {str(e)}")
        return error_response(f'Error deleting report: {str(e)}', 500)

def restore_report(event, user_email):
    """Restore a soft-deleted report"""
    try:
        # Extract report_id from path
        path_parts = event['path'].split('/')
        report_id = path_parts[-2]  # /reports/{id}/restore
        
        table = dynamodb.Table(REPORTS_TABLE)
        
        # Check if report exists and belongs to user
        response = table.get_item(
            Key={'report_id': report_id}
        )
        
        if 'Item' not in response:
            return error_response('Report not found', 404)
        
        report = response['Item']
        if report['user_email'] != user_email:
            return error_response('Unauthorized to restore this report', 403)
        
        if not report.get('is_deleted', False):
            return error_response('Report is not deleted', 400)
        
        # Restore report
        table.update_item(
            Key={'report_id': report_id},
            UpdateExpression='SET is_deleted = :deleted, deleted_at = :deleted_at, updated_at = :updated_at',
            ExpressionAttributeValues={
                ':deleted': False,
                ':deleted_at': None,
                ':updated_at': datetime.utcnow().isoformat()
            }
        )
        
        return success_response({'message': 'Report restored successfully'})
        
    except Exception as e:
        print(f"Error restoring report: {str(e)}")
        return error_response(f'Error restoring report: {str(e)}', 500)

def download_report(event, user_email):
    """Download a report file from S3"""
    try:
        # Extract report_id from path
        path_parts = event['path'].split('/')
        report_id = path_parts[-2]  # /reports/{id}/download
        
        table = dynamodb.Table(REPORTS_TABLE)
        
        # Get report metadata
        response = table.get_item(
            Key={'report_id': report_id}
        )
        
        if 'Item' not in response:
            return error_response('Report not found', 404)
        
        report = response['Item']
        if report['user_email'] != user_email:
            return error_response('Unauthorized to download this report', 403)
        
        if report.get('is_deleted', False):
            return error_response('Report is deleted', 404)
        
        # Get file from S3
        s3_response = s3_client.get_object(
            Bucket=REPORTS_BUCKET,
            Key=report['s3_key']
        )
        
        file_content = s3_response['Body'].read()
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': f'attachment; filename="{report["titulo"]}.py"'
            },
            'body': base64.b64encode(file_content).decode('utf-8'),
            'isBase64Encoded': True
        }
        
    except Exception as e:
        print(f"Error downloading report: {str(e)}")
        return error_response(f'Error downloading report: {str(e)}', 500)

def parse_multipart_form_data(body, content_type):
    """Parse multipart form data"""
    # Extract boundary
    boundary = content_type.split('boundary=')[1].encode()
    
    parts = body.split(b'--' + boundary)
    form_data = {}
    
    for part in parts[1:-1]:  # Skip first empty part and last closing part
        if not part.strip():
            continue
            
        # Split headers and content
        header_end = part.find(b'\r\n\r\n')
        if header_end == -1:
            continue
            
        headers = part[:header_end].decode('utf-8')
        content = part[header_end + 4:]
        
        # Remove trailing \r\n
        if content.endswith(b'\r\n'):
            content = content[:-2]
        
        # Parse Content-Disposition header
        for line in headers.split('\r\n'):
            if line.startswith('Content-Disposition:'):
                # Extract field name
                name_start = line.find('name="') + 6
                name_end = line.find('"', name_start)
                field_name = line[name_start:name_end]
                
                # Check if it's a file upload
                if 'filename=' in line:
                    filename_start = line.find('filename="') + 10
                    filename_end = line.find('"', filename_start)
                    filename = line[filename_start:filename_end]
                    
                    form_data[field_name] = {
                        'filename': filename,
                        'content': content
                    }
                else:
                    form_data[field_name] = content.decode('utf-8')
                break
    
    return form_data

def success_response(data):
    """Return success response with CORS headers"""
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(data)
    }

def error_response(message, status_code):
    """Return error response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'error': message})
    }
