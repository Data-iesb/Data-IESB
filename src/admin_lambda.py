import json
import boto3
import uuid
from datetime import datetime
import base64
from botocore.exceptions import ClientError
import jwt
from jwt.exceptions import InvalidTokenError

# AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Configuration
BUCKET_NAME = 'your-s3-bucket-name'  # Replace with your actual bucket name
REPORTS_TABLE = 'reports-table'  # Replace with your DynamoDB table name
COGNITO_USER_POOL_ID = 'your-user-pool-id'  # Replace with your Cognito User Pool ID
COGNITO_REGION = 'us-east-1'

# DynamoDB table
reports_table = dynamodb.Table(REPORTS_TABLE)

def lambda_handler(event, context):
    """
    Main Lambda handler for admin report management
    """
    try:
        # Extract user email from JWT token
        user_email = get_user_email_from_token(event)
        if not user_email:
            return create_response(401, 'Unauthorized')
        
        # Route based on HTTP method and path
        http_method = event['httpMethod']
        path = event['path']
        
        if http_method == 'GET' and path.endswith('/reports'):
            return get_user_reports(user_email)
        elif http_method == 'POST' and path.endswith('/reports'):
            return create_report(event, user_email)
        elif http_method == 'PUT' and '/reports/' in path:
            report_id = path.split('/reports/')[-1]
            return update_report(event, user_email, report_id)
        elif http_method == 'DELETE' and '/reports/' in path:
            report_id = path.split('/reports/')[-1]
            return delete_report(user_email, report_id)
        elif http_method == 'POST' and path.endswith('/restore'):
            report_id = path.split('/reports/')[-1].replace('/restore', '')
            return restore_report(user_email, report_id)
        else:
            return create_response(404, 'Not Found')
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return create_response(500, f'Internal Server Error: {str(e)}')

def get_user_email_from_token(event):
    """
    Extract user email from JWT token in Authorization header
    """
    try:
        auth_header = event.get('headers', {}).get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.replace('Bearer ', '')
        
        # Decode JWT without verification (for development)
        # In production, you should verify the token properly
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded.get('email')
        
    except Exception as e:
        print(f"Error decoding token: {str(e)}")
        return None

def get_user_reports(user_email):
    """
    Get all reports for a specific user
    """
    try:
        # Scan table for reports belonging to this user
        response = reports_table.scan(
            FilterExpression='user_email = :email',
            ExpressionAttributeValues={':email': user_email}
        )
        
        # Format response to match reports.json structure
        reports = {}
        for item in response['Items']:
            reports[item['report_id']] = {
                'id_s3': item['id_s3'],
                'descricao': item['descricao'],
                'deletado': item.get('deletado', False),
                'autor': item['autor'],
                'titulo': item['titulo']
            }
        
        return create_response(200, reports)
        
    except Exception as e:
        print(f"Error getting reports: {str(e)}")
        return create_response(500, f'Error retrieving reports: {str(e)}')

def create_report(event, user_email):
    """
    Create a new report
    """
    try:
        # Parse multipart form data
        form_data = parse_multipart_form_data(event)
        
        # Validate required fields
        required_fields = ['titulo', 'autor', 'descricao']
        for field in required_fields:
            if field not in form_data:
                return create_response(400, f'Missing required field: {field}')
        
        # Check if main.py file is provided
        if 'main' not in form_data:
            return create_response(400, 'main.py file is required')
        
        # Generate unique report ID
        report_id = str(uuid.uuid4())
        s3_path = f"reports/{report_id}/"
        
        # Upload main.py to S3
        main_file = form_data['main']
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=f"{s3_path}main.py",
            Body=main_file['content'],
            ContentType='text/x-python'
        )
        
        # Create report record in DynamoDB
        report_data = {
            'report_id': report_id,
            'user_email': user_email,
            'id_s3': s3_path,
            'titulo': form_data['titulo'],
            'autor': form_data['autor'],
            'descricao': form_data['descricao'],
            'deletado': False,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        reports_table.put_item(Item=report_data)
        
        return create_response(200, {'message': 'Report created successfully', 'report_id': report_id})
        
    except Exception as e:
        print(f"Error creating report: {str(e)}")
        return create_response(500, f'Error creating report: {str(e)}')

def update_report(event, user_email, report_id):
    """
    Update an existing report
    """
    try:
        # Check if report exists and belongs to user
        report = get_report_by_id(report_id, user_email)
        if not report:
            return create_response(404, 'Report not found or access denied')
        
        # Parse multipart form data
        form_data = parse_multipart_form_data(event)
        
        # Update fields
        update_expression = "SET updated_at = :updated_at"
        expression_values = {':updated_at': datetime.utcnow().isoformat()}
        
        if 'titulo' in form_data:
            update_expression += ", titulo = :titulo"
            expression_values[':titulo'] = form_data['titulo']
        
        if 'autor' in form_data:
            update_expression += ", autor = :autor"
            expression_values[':autor'] = form_data['autor']
        
        if 'descricao' in form_data:
            update_expression += ", descricao = :descricao"
            expression_values[':descricao'] = form_data['descricao']
        
        # Update main.py file if provided
        if 'main' in form_data:
            main_file = form_data['main']
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=f"{report['id_s3']}main.py",
                Body=main_file['content'],
                ContentType='text/x-python'
            )
        
        # Update DynamoDB record
        reports_table.update_item(
            Key={'report_id': report_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values
        )
        
        return create_response(200, {'message': 'Report updated successfully'})
        
    except Exception as e:
        print(f"Error updating report: {str(e)}")
        return create_response(500, f'Error updating report: {str(e)}')

def delete_report(user_email, report_id):
    """
    Soft delete a report (mark as deleted)
    """
    try:
        # Check if report exists and belongs to user
        report = get_report_by_id(report_id, user_email)
        if not report:
            return create_response(404, 'Report not found or access denied')
        
        # Mark as deleted
        reports_table.update_item(
            Key={'report_id': report_id},
            UpdateExpression="SET deletado = :deleted, updated_at = :updated_at",
            ExpressionAttributeValues={
                ':deleted': True,
                ':updated_at': datetime.utcnow().isoformat()
            }
        )
        
        return create_response(200, {'message': 'Report deleted successfully'})
        
    except Exception as e:
        print(f"Error deleting report: {str(e)}")
        return create_response(500, f'Error deleting report: {str(e)}')

def restore_report(user_email, report_id):
    """
    Restore a deleted report
    """
    try:
        # Check if report exists and belongs to user
        report = get_report_by_id(report_id, user_email)
        if not report:
            return create_response(404, 'Report not found or access denied')
        
        # Mark as not deleted
        reports_table.update_item(
            Key={'report_id': report_id},
            UpdateExpression="SET deletado = :deleted, updated_at = :updated_at",
            ExpressionAttributeValues={
                ':deleted': False,
                ':updated_at': datetime.utcnow().isoformat()
            }
        )
        
        return create_response(200, {'message': 'Report restored successfully'})
        
    except Exception as e:
        print(f"Error restoring report: {str(e)}")
        return create_response(500, f'Error restoring report: {str(e)}')

def get_report_by_id(report_id, user_email):
    """
    Get a specific report by ID and verify ownership
    """
    try:
        response = reports_table.get_item(Key={'report_id': report_id})
        
        if 'Item' not in response:
            return None
        
        report = response['Item']
        
        # Check if user owns this report
        if report.get('user_email') != user_email:
            return None
        
        return report
        
    except Exception as e:
        print(f"Error getting report by ID: {str(e)}")
        return None

def parse_multipart_form_data(event):
    """
    Parse multipart form data from API Gateway event
    """
    try:
        content_type = event.get('headers', {}).get('content-type', '')
        if 'multipart/form-data' not in content_type:
            return {}
        
        # Extract boundary
        boundary = content_type.split('boundary=')[1]
        
        # Decode body
        body = base64.b64decode(event['body']) if event.get('isBase64Encoded') else event['body'].encode()
        
        # Parse multipart data
        form_data = {}
        parts = body.split(f'--{boundary}'.encode())
        
        for part in parts[1:-1]:  # Skip first empty part and last boundary
            if not part.strip():
                continue
            
            # Split headers and content
            header_end = part.find(b'\r\n\r\n')
            if header_end == -1:
                continue
            
            headers = part[:header_end].decode()
            content = part[header_end + 4:]
            
            # Extract field name
            name_match = headers.split('name="')[1].split('"')[0] if 'name="' in headers else None
            if not name_match:
                continue
            
            # Check if it's a file
            if 'filename=' in headers:
                filename = headers.split('filename="')[1].split('"')[0]
                form_data[name_match] = {
                    'filename': filename,
                    'content': content.rstrip(b'\r\n')
                }
            else:
                form_data[name_match] = content.decode().rstrip('\r\n')
        
        return form_data
        
    except Exception as e:
        print(f"Error parsing form data: {str(e)}")
        return {}

def create_response(status_code, body):
    """
    Create HTTP response
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': json.dumps(body) if isinstance(body, (dict, list)) else str(body)
    }
