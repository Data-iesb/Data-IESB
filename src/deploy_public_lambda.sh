#!/bin/bash

# Deployment script for DataIESB Public Reports Lambda Function
# This script will package and deploy the public Lambda function

set -e

LAMBDA_FUNCTION_NAME="dataiesb-public-reports"
REGION="us-east-1"

echo "🚀 Starting deployment of DataIESB Public Reports Lambda Function..."

# Create deployment package
echo "📦 Creating deployment package..."
rm -rf public-lambda-package
mkdir public-lambda-package
cp lambda-public/public_reports_lambda.py public-lambda-package/lambda_function.py

# Create requirements.txt for Lambda
cat > public-lambda-package/requirements.txt << EOF
boto3>=1.26.0
botocore>=1.29.0
EOF

# Package the Lambda function
cd public-lambda-package
zip -r ../public-lambda-deployment.zip .
cd ..

echo "📋 Lambda function configuration:"
echo "  - Function Name: $LAMBDA_FUNCTION_NAME"
echo "  - Region: $REGION"

# Check if Lambda function exists
if aws lambda get-function --function-name $LAMBDA_FUNCTION_NAME --region $REGION >/dev/null 2>&1; then
    echo "🔄 Updating existing Lambda function..."
    aws lambda update-function-code \
        --function-name $LAMBDA_FUNCTION_NAME \
        --zip-file fileb://public-lambda-deployment.zip \
        --region $REGION
    
    echo "⚙️ Updating environment variables..."
    aws lambda update-function-configuration \
        --function-name $LAMBDA_FUNCTION_NAME \
        --environment Variables="{REPORTS_TABLE=dataiesb-reports}" \
        --region $REGION
else
    echo "❌ Lambda function $LAMBDA_FUNCTION_NAME not found!"
    echo "Please create the Lambda function first or update the function name."
    exit 1
fi

# Clean up
rm -rf public-lambda-package public-lambda-deployment.zip

echo ""
echo "✅ Public Lambda deployment completed successfully!"
echo ""
echo "📝 Summary:"
echo "  - Fixed filter expression to properly exclude deleted reports"
echo "  - Now only returns reports where is_deleted = false"
echo "  - Deleted reports (5, 6, 9) should no longer appear in public API"
