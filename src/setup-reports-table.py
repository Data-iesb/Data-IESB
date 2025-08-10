#!/usr/bin/env python3
"""
Script to create DynamoDB table for reports management
"""

import boto3
from botocore.exceptions import ClientError

def create_reports_table():
    """
    Create DynamoDB table for storing report metadata
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    table_name = 'dataiesb-reports'
    
    try:
        # Check if table already exists
        existing_table = dynamodb.Table(table_name)
        existing_table.load()
        print(f"Table {table_name} already exists")
        return existing_table
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceNotFoundException':
            raise
    
    # Create table
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'report_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'report_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'user_email',
                'AttributeType': 'S'
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'user-email-index',
                'KeySchema': [
                    {
                        'AttributeName': 'user_email',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                }
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    
    # Wait for table to be created
    print(f"Creating table {table_name}...")
    table.wait_until_exists()
    print(f"Table {table_name} created successfully!")
    
    return table

def migrate_existing_reports():
    """
    Migrate existing reports from reports.json to DynamoDB
    This is optional and should be run only once
    """
    import json
    import uuid
    from datetime import datetime
    
    # Read existing reports.json
    try:
        with open('reports.json', 'r', encoding='utf-8') as f:
            reports_data = json.load(f)
    except FileNotFoundError:
        print("reports.json not found, skipping migration")
        return
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('dataiesb-reports')
    
    # Default email for existing reports (you should update this)
    default_email = "admin@dataiesb.com"
    
    print("Migrating existing reports...")
    
    for report_id, report_data in reports_data.items():
        # Create new record in DynamoDB
        item = {
            'report_id': report_id,
            'user_email': default_email,  # You may want to map this properly
            'id_s3': report_data['id_s3'],
            'titulo': report_data['titulo'],
            'autor': report_data['autor'],
            'descricao': report_data['descricao'],
            'deletado': report_data.get('deletado', False),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        table.put_item(Item=item)
        print(f"Migrated report: {report_data['titulo']}")
    
    print("Migration completed!")

if __name__ == "__main__":
    import sys
    
    # Create table
    table = create_reports_table()
    
    # Ask if user wants to migrate existing data
    if len(sys.argv) > 1 and sys.argv[1] == '--migrate':
        migrate_existing_reports()
    else:
        print("\nTo migrate existing reports from reports.json, run:")
        print("python setup-reports-table.py --migrate")
