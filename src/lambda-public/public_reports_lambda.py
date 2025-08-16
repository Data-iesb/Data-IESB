import json
import boto3
from decimal import Decimal
import os

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('REPORTS_TABLE', 'dataiesb-reports')

def lambda_handler(event, context):
    """
    Lambda function to serve public reports from DynamoDB
    Returns all non-deleted reports for public consumption
    """
    
    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            }
        }
    
    try:
        # Get the DynamoDB table
        table = dynamodb.Table(table_name)
        
        # Scan the table for all non-deleted reports
        # Fixed filter: only return records where is_deleted is false
        response = table.scan(
            FilterExpression='is_deleted = :deleted',
            ExpressionAttributeValues={
                ':deleted': False
            }
        )
        
        # Process the items
        reports = {}
        for item in response['Items']:
            report_id = item['report_id']
            
            # Convert Decimal types to regular numbers for JSON serialization
            processed_item = {}
            for key, value in item.items():
                if isinstance(value, Decimal):
                    # Convert Decimal to int or float
                    processed_item[key] = int(value) if value % 1 == 0 else float(value)
                else:
                    processed_item[key] = value
            
            # Create the public report structure
            public_report = {
                'titulo': processed_item.get('titulo', ''),
                'autor': processed_item.get('autor', ''),
                'descricao': processed_item.get('descricao', ''),
                'created_at': processed_item.get('created_at', ''),
                'updated_at': processed_item.get('updated_at', ''),
                # Correct id_s3 format - just the report ID
                'id_s3': report_id,
                'deletado': False  # All returned reports are non-deleted
            }
            
            reports[report_id] = public_report
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(reports)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': f'Internal server error: {str(e)}'
            })
        }
