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
        
        method = event['httpMethod']
        path = event.get('path', '')
        
        # Handle login endpoint (no authentication required)
        if method == 'POST' and (path == '/dataiesb-auth' or path.endswith('/dataiesb-auth')):
            return handle_login(event)
        
        # Get user info from JWT token for all other endpoints
        user_email = get_user_from_token(event.get('headers', {}).get('Authorization', ''))
        if not user_email:
            return error_response('Unauthorized', 401)
        
        method = event['httpMethod']
        path = event.get('path', '')
        query_params = event.get('queryStringParameters') or {}
        
        # Handle query parameter actions for API Gateway routing workaround
        if query_params.get('action'):
            action = query_params.get('action')
            report_id = query_params.get('id')
            
            if action == 'download' and method == 'GET':
                # Simulate download path for query parameter
                event['path'] = f"/dataiesb-auth/reports/{report_id}/download"
                return download_report(event, user_email)
            elif action == 'update' and method == 'POST':
                # Simulate update path for query parameter (using POST instead of PUT)
                event['path'] = f"/dataiesb-auth/reports/{report_id}"
                event['httpMethod'] = 'PUT'  # Change method to PUT for internal processing
                return update_report_metadata(event, user_email)
            elif action == 'restore' and method == 'POST':
                # Simulate restore path for query parameter
                event['path'] = f"/dataiesb-auth/reports/{report_id}/restore"
                return restore_report(event, user_email)
            elif action == 'save-code' and method == 'POST':
                # Simulate save code path for query parameter
                event['path'] = f"/dataiesb-auth/reports/{report_id}/code"
                event['httpMethod'] = 'PUT'  # Change method to PUT for internal processing
                return update_report_code(event, user_email)
        
        if method == 'POST' and '/reports' in path:
            # Check if it's a restore request (old path-based approach)
            if '/restore' in path:
                return restore_report(event, user_email)
            # Otherwise it's a create request
            return create_report(event, user_email)
        elif method == 'GET' and '/reports' in path:
            if '/download' in path:
                return download_report(event, user_email)
            elif '/code' in path:
                return get_report_code(event, user_email)
            else:
                # Check if requesting deleted reports
                if query_params.get('deleted') == 'true':
                    return list_deleted_reports(user_email)
                else:
                    return list_reports(user_email)
        elif method == 'PUT' and '/reports' in path:
            if '/restore' in path:
                return restore_report(event, user_email)
            elif '/code' in path:
                return update_report_code(event, user_email)
            elif '/status' in path:
                return update_report_status(event, user_email)
            elif '/metadata' in path:
                return update_report_metadata(event, user_email)
            else:
                # Default PUT to /reports/{id} should update metadata
                return update_report_metadata(event, user_email)
        elif method == 'DELETE' and '/reports' in path:
            return soft_delete_report(event, user_email)
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
        
        # Get initial status (default to 'active')
        initial_status = form_data.get('status', 'active')
        valid_statuses = ['active', 'inactive', 'draft']
        if initial_status not in valid_statuses:
            initial_status = 'active'
        
        # Generate incremental ID for the report
        report_id = get_next_report_id()
        timestamp = datetime.utcnow().isoformat()
        
        # Upload Python file to correct S3 bucket (dataiesb-reports)
        file_key = f"{report_id}/"
        s3_object_key = f"{file_key}main.py"
        
        s3_client.put_object(
            Bucket=REPORTS_BUCKET,
            Key=s3_object_key,
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
                'id_s3': file_key,  # Store the S3 prefix, not the full key
                'status': initial_status,  # Add status field
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
            's3_key': s3_object_key
        })
        
    except Exception as e:
        print(f"Error creating report: {str(e)}")
        return error_response(f'Error creating report: {str(e)}', 500)

def list_deleted_reports(user_email):
    """List all deleted reports for the user"""
    try:
        table = dynamodb.Table(REPORTS_TABLE)
        
        response = table.scan(
            FilterExpression='user_email = :user_email AND is_deleted = :is_deleted',
            ExpressionAttributeValues={
                ':user_email': user_email,
                ':is_deleted': True
            }
        )
        
        reports = {}
        for item in response['Items']:
            reports[item['report_id']] = {
                'titulo': item['titulo'],
                'autor': item['autor'],
                'descricao': item['descricao'],
                'created_at': item['created_at'],
                'updated_at': item['updated_at'],
                'deleted_at': item.get('deleted_at')
            }
        
        return success_response(reports)
        
    except Exception as e:
        print(f"Error listing deleted reports: {str(e)}")
        return error_response(f'Error listing deleted reports: {str(e)}', 500)

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
                'status': item.get('status', 'active'),  # Include status
                'created_at': item['created_at'],
                'updated_at': item['updated_at']
            }
        
        return success_response(reports)
        
    except Exception as e:
        print(f"Error listing reports: {str(e)}")
        return error_response(f'Error listing reports: {str(e)}', 500)

def soft_delete_report(event, user_email):
    """Soft delete a report (mark as deleted) or permanently delete if permanent=true"""
    try:
        # Extract report_id from path
        path_parts = event['path'].split('/')
        report_id = path_parts[-1]
        
        # Check if this is a permanent deletion
        query_params = event.get('queryStringParameters') or {}
        is_permanent = query_params.get('permanent') == 'true'
        
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
        
        if is_permanent:
            # Permanent deletion - remove from DynamoDB and S3
            try:
                # Delete from S3 first
                s3_key = f"{report['id_s3']}main.py"
                s3_client.delete_object(
                    Bucket=REPORTS_BUCKET,
                    Key=s3_key
                )
                
                # Also delete any backup files
                try:
                    backup_prefix = f"{report['id_s3']}main_backup_"
                    backup_objects = s3_client.list_objects_v2(
                        Bucket=REPORTS_BUCKET,
                        Prefix=backup_prefix
                    )
                    
                    if 'Contents' in backup_objects:
                        for obj in backup_objects['Contents']:
                            s3_client.delete_object(
                                Bucket=REPORTS_BUCKET,
                                Key=obj['Key']
                            )
                except:
                    # If backup deletion fails, continue anyway
                    pass
                
                # Delete from DynamoDB
                table.delete_item(
                    Key={'report_id': report_id}
                )
                
                return success_response({
                    'message': 'Report permanently deleted',
                    'deleted_files': [s3_key],
                    'report_id': report_id
                })
                
            except Exception as s3_error:
                print(f"Error deleting S3 files: {str(s3_error)}")
                return error_response(f'Error deleting files: {str(s3_error)}', 500)
        else:
            # Soft delete - mark as deleted
            if report.get('is_deleted', False):
                return error_response('Report already deleted', 400)
            
            table.update_item(
                Key={'report_id': report_id},
                UpdateExpression='SET is_deleted = :deleted, deleted_at = :deleted_at, updated_at = :updated_at',
                ExpressionAttributeValues={
                    ':deleted': True,
                    ':deleted_at': datetime.utcnow().isoformat(),
                    ':updated_at': datetime.utcnow().isoformat()
                }
            )
            
            return success_response({'message': 'Report hidden successfully'})
        
    except Exception as e:
        print(f"Error deleting report: {str(e)}")
        return error_response(f'Error deleting report: {str(e)}', 500)

def restore_report(event, user_email):
    """Restore a soft-deleted report"""
    try:
        # Extract report_id from path
        path_parts = event['path'].split('/')
        
        # Handle different path formats:
        # /reports/{id}/restore -> path_parts[-2]
        # /reports/{id} -> path_parts[-1]
        if path_parts[-1] == 'restore':
            report_id = path_parts[-2]  # /reports/{id}/restore
        else:
            report_id = path_parts[-1]  # /reports/{id}
        
        print(f"Restore: Extracting report_id from path: {event['path']} -> {report_id}")
        
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
        
        # Handle different path formats:
        # /reports/{id}/download -> path_parts[-2]
        # /reports/{id} -> path_parts[-1]
        if path_parts[-1] == 'download':
            report_id = path_parts[-2]  # /reports/{id}/download
        else:
            report_id = path_parts[-1]  # /reports/{id}
        
        print(f"Download: Extracting report_id from path: {event['path']} -> {report_id}")
        
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
        
        # Construct S3 key from id_s3 column
        s3_key = f"{report['id_s3']}main.py"
        
        # Get file from S3
        s3_response = s3_client.get_object(
            Bucket=REPORTS_BUCKET,
            Key=s3_key
        )
        
        file_content = s3_response['Body'].read()
        
        # Check if this is for code editing (query parameter approach) or file download
        query_params = event.get('queryStringParameters') or {}
        is_code_editing = query_params.get('action') == 'download'
        
        if is_code_editing:
            # For code editing, return as plain text
            try:
                # Decode as UTF-8 text
                text_content = file_content.decode('utf-8')
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'text/plain; charset=utf-8'
                    },
                    'body': text_content
                }
            except UnicodeDecodeError:
                # If it's not valid UTF-8, fall back to base64
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
        else:
            # For file download, return as binary
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

def get_report_code(event, user_email):
    """Get the Python code for a report"""
    try:
        # Extract report_id from path
        path_parts = event['path'].split('/')
        report_id = path_parts[-2]  # /reports/{id}/code
        
        table = dynamodb.Table(REPORTS_TABLE)
        
        # Get report metadata
        response = table.get_item(
            Key={'report_id': report_id}
        )
        
        if 'Item' not in response:
            return error_response('Report not found', 404)
        
        report = response['Item']
        if report['user_email'] != user_email:
            return error_response('Unauthorized to access this report', 403)
        
        if report.get('is_deleted', False):
            return error_response('Report is deleted', 404)
        
        # Construct S3 key from id_s3 column
        s3_key = f"{report['id_s3']}main.py"
        
        # Get file from S3
        s3_response = s3_client.get_object(
            Bucket=REPORTS_BUCKET,
            Key=s3_key
        )
        
        file_content = s3_response['Body'].read().decode('utf-8')
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'text/plain'
            },
            'body': file_content
        }
        
    except Exception as e:
        print(f"Error getting report code: {str(e)}")
        return error_response(f'Error getting report code: {str(e)}', 500)

def update_report_code(event, user_email):
    """Update the Python code for a report"""
    try:
        # Extract report_id from path
        path_parts = event['path'].split('/')
        
        # Handle different path formats:
        # /reports/{id}/code -> path_parts[-2]
        # /reports/{id} -> path_parts[-1]
        if path_parts[-1] == 'code':
            report_id = path_parts[-2]  # /reports/{id}/code
        else:
            report_id = path_parts[-1]  # /reports/{id}
        
        print(f"Save Code: Extracting report_id from path: {event['path']} -> {report_id}")
        
        # Parse request body
        body = json.loads(event['body'])
        new_code = body.get('code', '')
        
        if not new_code:
            return error_response('Code content is required', 400)
        
        table = dynamodb.Table(REPORTS_TABLE)
        
        # Get report metadata
        response = table.get_item(
            Key={'report_id': report_id}
        )
        
        if 'Item' not in response:
            return error_response('Report not found', 404)
        
        report = response['Item']
        if report['user_email'] != user_email:
            return error_response('Unauthorized to update this report', 403)
        
        if report.get('is_deleted', False):
            return error_response('Cannot update deleted report', 400)
        
        # Construct S3 key from id_s3 column
        s3_key = f"{report['id_s3']}main.py"
        
        # Create backup of current file
        backup_key = f"{report['id_s3']}main_backup_{int(datetime.utcnow().timestamp())}.py"
        
        try:
            # Copy current file to backup
            s3_client.copy_object(
                Bucket=REPORTS_BUCKET,
                CopySource={'Bucket': REPORTS_BUCKET, 'Key': s3_key},
                Key=backup_key
            )
        except:
            # If backup fails, continue anyway
            pass
        
        # Upload new code to S3
        s3_client.put_object(
            Bucket=REPORTS_BUCKET,
            Key=s3_key,
            Body=new_code.encode('utf-8'),
            ContentType='text/x-python',
            Metadata={
                'user': user_email,
                'report_id': report_id,
                'updated_by': 'admin_panel'
            }
        )
        
        # Update timestamp in DynamoDB
        table.update_item(
            Key={'report_id': report_id},
            UpdateExpression='SET updated_at = :updated_at',
            ExpressionAttributeValues={
                ':updated_at': datetime.utcnow().isoformat()
            }
        )
        
        return success_response({
            'message': 'Code updated successfully',
            'backup_created': backup_key
        })
        
    except Exception as e:
        print(f"Error updating report code: {str(e)}")
        return error_response(f'Error updating report code: {str(e)}', 500)

def update_report_status(event, user_email):
    """Update the status of a report"""
    try:
        # Extract report_id from path
        path_parts = event['path'].split('/')
        report_id = path_parts[-2]  # /reports/{id}/status
        
        # Parse request body
        body = json.loads(event['body'])
        new_status = body.get('status', '')
        
        valid_statuses = ['active', 'inactive', 'draft']
        if new_status not in valid_statuses:
            return error_response(f'Invalid status. Must be one of: {", ".join(valid_statuses)}', 400)
        
        table = dynamodb.Table(REPORTS_TABLE)
        
        # Get report metadata
        response = table.get_item(
            Key={'report_id': report_id}
        )
        
        if 'Item' not in response:
            return error_response('Report not found', 404)
        
        report = response['Item']
        if report['user_email'] != user_email:
            return error_response('Unauthorized to update this report', 403)
        
        if report.get('is_deleted', False):
            return error_response('Cannot update status of deleted report', 400)
        
        # Update status in DynamoDB
        table.update_item(
            Key={'report_id': report_id},
            UpdateExpression='SET #status = :status, updated_at = :updated_at',
            ExpressionAttributeNames={
                '#status': 'status'  # 'status' is a reserved word in DynamoDB
            },
            ExpressionAttributeValues={
                ':status': new_status,
                ':updated_at': datetime.utcnow().isoformat()
            }
        )
        
        return success_response({
            'message': f'Status updated to {new_status}',
            'report_id': report_id,
            'new_status': new_status
        })
        
    except Exception as e:
        print(f"Error updating report status: {str(e)}")
        return error_response(f'Error updating report status: {str(e)}', 500)

def update_report_metadata(event, user_email):
    """Update the metadata (titulo, autor, descricao) of a report"""
    try:
        # Extract report_id from path
        path_parts = event['path'].split('/')
        
        # Handle different path formats:
        # /reports/{id}/metadata -> path_parts[-2]
        # /reports/{id} -> path_parts[-1]
        if path_parts[-1] == 'metadata':
            report_id = path_parts[-2]  # /reports/{id}/metadata
        else:
            report_id = path_parts[-1]  # /reports/{id}
        
        print(f"Extracting report_id from path: {event['path']} -> {report_id}")
        
        # Parse request body
        body = json.loads(event['body'])
        titulo = body.get('titulo', '').strip()
        autor = body.get('autor', '').strip()
        descricao = body.get('descricao', '').strip()
        
        if not titulo or not autor or not descricao:
            return error_response('Título, autor e descrição são obrigatórios', 400)
        
        table = dynamodb.Table(REPORTS_TABLE)
        
        # Get report metadata
        response = table.get_item(
            Key={'report_id': report_id}
        )
        
        if 'Item' not in response:
            return error_response('Report not found', 404)
        
        report = response['Item']
        if report['user_email'] != user_email:
            return error_response('Unauthorized to update this report', 403)
        
        if report.get('is_deleted', False):
            return error_response('Cannot update metadata of deleted report', 400)
        
        # Update metadata in DynamoDB
        table.update_item(
            Key={'report_id': report_id},
            UpdateExpression='SET titulo = :titulo, autor = :autor, descricao = :descricao, updated_at = :updated_at',
            ExpressionAttributeValues={
                ':titulo': titulo,
                ':autor': autor,
                ':descricao': descricao,
                ':updated_at': datetime.utcnow().isoformat()
            }
        )
        
        return success_response({
            'message': 'Metadata updated successfully',
            'report_id': report_id,
            'titulo': titulo,
            'autor': autor,
            'descricao': descricao
        })
        
    except Exception as e:
        print(f"Error updating report metadata: {str(e)}")
        return error_response(f'Error updating report metadata: {str(e)}', 500)

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

def handle_login(event):
    """Handle user login with AWS Cognito"""
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        username = body.get('username', '').strip()
        password = body.get('password', '').strip()
        
        if not username or not password:
            return error_response('Username and password are required', 400)
        
        # Validate IESB domain
        if not username.endswith('@iesb.edu.br'):
            return error_response('Only @iesb.edu.br emails are allowed', 400)
        
        # Initialize Cognito client
        cognito_client = boto3.client('cognito-idp', region_name='us-east-1')
        
        # Cognito User Pool configuration
        USER_POOL_ID = 'us-east-1_QvLQs82bE'  # Actual pool ID from AWS
        CLIENT_ID = '2mpcqrmv19qk8ajqk9j2cemimj'  # From your login.html
        
        try:
            # Authenticate with Cognito
            response = cognito_client.admin_initiate_auth(
                UserPoolId=USER_POOL_ID,
                ClientId=CLIENT_ID,
                AuthFlow='ADMIN_NO_SRP_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            
            # Extract tokens
            auth_result = response['AuthenticationResult']
            id_token = auth_result['IdToken']
            access_token = auth_result['AccessToken']
            refresh_token = auth_result['RefreshToken']
            
            return success_response({
                'message': 'Login successful',
                'idToken': id_token,
                'accessToken': access_token,
                'refreshToken': refresh_token
            })
            
        except cognito_client.exceptions.NotAuthorizedException:
            return error_response('Invalid username or password', 401)
        except cognito_client.exceptions.UserNotConfirmedException:
            return error_response('User account not confirmed. Please check your email.', 401)
        except cognito_client.exceptions.UserNotFoundException:
            return error_response('User not found', 401)
        except Exception as cognito_error:
            print(f"Cognito error: {str(cognito_error)}")
            return error_response('Authentication service error', 500)
            
    except json.JSONDecodeError:
        return error_response('Invalid JSON in request body', 400)
    except Exception as e:
        print(f"Login error: {str(e)}")
        return error_response('Internal server error during login', 500)

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
