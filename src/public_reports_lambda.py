import json
import boto3
from botocore.exceptions import ClientError

# AWS clients
dynamodb = boto3.resource('dynamodb')

# Configuration
REPORTS_TABLE = 'dataiesb-reports'  # Replace with your DynamoDB table name

# DynamoDB table
reports_table = dynamodb.Table(REPORTS_TABLE)

def lambda_handler(event, context):
    """
    Lambda handler to serve public reports data
    This endpoint doesn't require authentication and only returns non-deleted reports
    """
    try:
        # Handle CORS preflight requests
        if event.get('httpMethod') == 'OPTIONS':
            return create_response(200, 'OK')
        
        # Get all non-deleted reports
        reports = get_public_reports()
        
        return create_response(200, reports)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return create_response(500, f'Internal Server Error: {str(e)}')

def get_public_reports():
    """
    Get all non-deleted reports for public display
    """
    try:
        # Scan table for non-deleted reports
        response = reports_table.scan(
            FilterExpression='deletado = :deleted',
            ExpressionAttributeValues={':deleted': False}
        )
        
        # Format response to match the original reports.json structure
        reports = {}
        for item in response['Items']:
            # Use a sequential ID for public display (you might want to use a different approach)
            report_id = item['report_id']
            
            reports[report_id] = {
                'id_s3': item['id_s3'],
                'descricao': item['descricao'],
                'deletado': False,  # Only non-deleted reports are returned
                'autor': item['autor'],
                'titulo': item['titulo']
            }
        
        return reports
        
    except Exception as e:
        print(f"Error getting public reports: {str(e)}")
        return {}

def create_response(status_code, body):
    """
    Create HTTP response with CORS headers
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Cache-Control': 'max-age=300'  # Cache for 5 minutes
        },
        'body': json.dumps(body) if isinstance(body, (dict, list)) else str(body)
    }
