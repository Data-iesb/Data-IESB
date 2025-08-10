import json
import boto3
import uuid
import base64
from datetime import datetime
from botocore.exceptions import ClientError
import jwt
from jwt.exceptions import InvalidTokenError

# AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
cognito_client = boto3.client('cognito-idp')

# Configuration
BUCKET_NAME = 'dataiesb'
REPORTS_TABLE = 'dataiesb-reports'
COGNITO_USER_POOL_ID = 'us-east-1_QvLQs82bE'
COGNITO_REGION = 'us-east-1'

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

def create_user_report(event, user_email, headers):
    """Create a new report for the user"""
    try:
        # Parse multipart form data
        content_type = event.get('headers', {}).get('content-type', '')
        if 'multipart/form-data' not in content_type:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Content-Type must be multipart/form-data'})
            }
        
        # For now, just create a simple report entry
        report_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Create DynamoDB entry
        table.put_item(
            Item={
                'report_id': report_id,
                'user_email': user_email,
                'titulo': 'New Report',  # Will be updated when we parse form data
                'autor': user_email.split('@')[0],  # Use email username as default author
                'descricao': 'Report created via admin interface',
                'created_at': timestamp,
                'updated_at': timestamp,
                'deletado': False,
                'id_s3': f'reports/{report_id}/'
            }
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Report created successfully',
                'report_id': report_id
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
        
        # Update report
        timestamp = datetime.utcnow().isoformat()
        table.update_item(
            Key={'report_id': report_id},
            UpdateExpression='SET updated_at = :timestamp',
            ExpressionAttributeValues={':timestamp': timestamp}
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
