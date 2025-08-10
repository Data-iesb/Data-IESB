#!/bin/bash

# Deployment script for Reports API
# This script creates Lambda functions and API Gateway endpoints for the reports system

set -e

# Configuration
REGION="us-east-1"
LAMBDA_ROLE_NAME="dataiesb-lambda-execution-role"
API_GATEWAY_NAME="dataiesb-reports-api"
STAGE_NAME="prod"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting deployment of Reports API...${NC}"

# Function to check if AWS CLI is configured
check_aws_cli() {
    if ! aws sts get-caller-identity > /dev/null 2>&1; then
        echo -e "${RED}Error: AWS CLI is not configured or credentials are invalid${NC}"
        echo "Please run 'aws configure' to set up your credentials"
        exit 1
    fi
    echo -e "${GREEN}✓ AWS CLI is configured${NC}"
}

# Function to create IAM role for Lambda
create_lambda_role() {
    echo -e "${YELLOW}Creating Lambda execution role...${NC}"
    
    # Check if role already exists
    if aws iam get-role --role-name $LAMBDA_ROLE_NAME > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Lambda role already exists${NC}"
        return
    fi

    # Create trust policy
    cat > trust-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF

    # Create role
    aws iam create-role \
        --role-name $LAMBDA_ROLE_NAME \
        --assume-role-policy-document file://trust-policy.json

    # Attach basic Lambda execution policy
    aws iam attach-role-policy \
        --role-name $LAMBDA_ROLE_NAME \
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

    # Create and attach DynamoDB policy
    cat > dynamodb-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem",
                "dynamodb:Scan",
                "dynamodb:Query"
            ],
            "Resource": [
                "arn:aws:dynamodb:${REGION}:*:table/dataiesb-reports",
                "arn:aws:dynamodb:${REGION}:*:table/dataiesb-reports/index/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::your-s3-bucket-name/*"
        }
    ]
}
EOF

    aws iam put-role-policy \
        --role-name $LAMBDA_ROLE_NAME \
        --policy-name DynamoDBAndS3Access \
        --policy-document file://dynamodb-policy.json

    # Clean up temporary files
    rm trust-policy.json dynamodb-policy.json

    echo -e "${GREEN}✓ Lambda execution role created${NC}"
    
    # Wait for role to be available
    echo "Waiting for role to be available..."
    sleep 10
}

# Function to create Lambda function
create_lambda_function() {
    local function_name=$1
    local python_file=$2
    local description=$3
    
    echo -e "${YELLOW}Creating Lambda function: $function_name${NC}"
    
    # Create deployment package
    zip -j ${function_name}.zip $python_file
    
    # Get role ARN
    ROLE_ARN=$(aws iam get-role --role-name $LAMBDA_ROLE_NAME --query 'Role.Arn' --output text)
    
    # Check if function already exists
    if aws lambda get-function --function-name $function_name > /dev/null 2>&1; then
        echo -e "${YELLOW}Function exists, updating code...${NC}"
        aws lambda update-function-code \
            --function-name $function_name \
            --zip-file fileb://${function_name}.zip
    else
        # Create function
        aws lambda create-function \
            --function-name $function_name \
            --runtime python3.9 \
            --role $ROLE_ARN \
            --handler ${python_file%.*}.lambda_handler \
            --zip-file fileb://${function_name}.zip \
            --description "$description" \
            --timeout 30 \
            --memory-size 256
    fi
    
    # Clean up zip file
    rm ${function_name}.zip
    
    echo -e "${GREEN}✓ Lambda function $function_name created/updated${NC}"
}

# Function to create API Gateway
create_api_gateway() {
    echo -e "${YELLOW}Setting up API Gateway...${NC}"
    
    # This is a simplified version - you'll need to configure the actual API Gateway
    # through the AWS Console or use more detailed AWS CLI commands
    
    echo -e "${YELLOW}Note: API Gateway setup requires manual configuration${NC}"
    echo "Please configure the following endpoints in API Gateway:"
    echo "  GET  /public-reports -> dataiesb-public-reports-function"
    echo "  GET  /reports -> dataiesb-admin-reports-function"
    echo "  POST /reports -> dataiesb-admin-reports-function"
    echo "  PUT  /reports/{id} -> dataiesb-admin-reports-function"
    echo "  DELETE /reports/{id} -> dataiesb-admin-reports-function"
    echo "  POST /reports/{id}/restore -> dataiesb-admin-reports-function"
}

# Main deployment process
main() {
    echo -e "${GREEN}=== DataIESB Reports API Deployment ===${NC}"
    
    # Check prerequisites
    check_aws_cli
    
    # Create DynamoDB table first
    echo -e "${YELLOW}Creating DynamoDB table...${NC}"
    python3 setup-reports-table.py
    
    # Create IAM role
    create_lambda_role
    
    # Create Lambda functions
    create_lambda_function "dataiesb-public-reports-function" "public_reports_lambda.py" "Serves public reports data from DynamoDB"
    create_lambda_function "dataiesb-admin-reports-function" "admin_lambda.py" "Handles admin CRUD operations for reports"
    
    # Setup API Gateway (manual step)
    create_api_gateway
    
    echo -e "${GREEN}=== Deployment Complete ===${NC}"
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Configure API Gateway endpoints manually"
    echo "2. Update the API endpoint URL in index.html and admin.html"
    echo "3. Update the S3 bucket name in the Lambda functions"
    echo "4. Test the endpoints"
}

# Run main function
main
