#!/bin/bash

# Deployment script for DataIESB Reports Lambda Function
# This script will package and deploy the Lambda function with correct S3 bucket configuration

set -e

LAMBDA_FUNCTION_NAME="dataiesb-admin-reports"
REPORTS_BUCKET="dataiesb-reports"
DATASETS_BUCKET="dataiesb-datasets"
REGION="us-east-1"

echo "🚀 Starting deployment of DataIESB Reports Lambda Function..."

# Create deployment package
echo "📦 Creating deployment package..."
rm -rf lambda-package
mkdir lambda-package
cp lambda/lambda_function.py lambda-package/

# Create requirements.txt for Lambda
cat > lambda-package/requirements.txt << EOF
boto3>=1.26.0
botocore>=1.29.0
EOF

# Package the Lambda function
cd lambda-package
zip -r ../lambda-deployment.zip .
cd ..

echo "📋 Lambda function configuration:"
echo "  - Function Name: $LAMBDA_FUNCTION_NAME"
echo "  - Reports Bucket: $REPORTS_BUCKET (for Python files)"
echo "  - Datasets Bucket: $DATASETS_BUCKET (for data files)"
echo "  - Region: $REGION"

# Check if Lambda function exists
if aws lambda get-function --function-name $LAMBDA_FUNCTION_NAME --region $REGION >/dev/null 2>&1; then
    echo "🔄 Updating existing Lambda function..."
    aws lambda update-function-code \
        --function-name $LAMBDA_FUNCTION_NAME \
        --zip-file fileb://lambda-deployment.zip \
        --region $REGION
    
    echo "⚙️ Updating environment variables..."
    aws lambda update-function-configuration \
        --function-name $LAMBDA_FUNCTION_NAME \
        --environment Variables="{REPORTS_TABLE=dataiesb-reports,REPORTS_BUCKET=$REPORTS_BUCKET,DATASETS_BUCKET=$DATASETS_BUCKET}" \
        --region $REGION
else
    echo "❌ Lambda function $LAMBDA_FUNCTION_NAME not found!"
    echo "Please create the Lambda function first or update the function name."
    echo ""
    echo "To create the function, you can use:"
    echo "aws lambda create-function \\"
    echo "  --function-name $LAMBDA_FUNCTION_NAME \\"
    echo "  --runtime python3.9 \\"
    echo "  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \\"
    echo "  --handler lambda_function.lambda_handler \\"
    echo "  --zip-file fileb://lambda-deployment.zip \\"
    echo "  --environment Variables='{REPORTS_TABLE=dataiesb-reports,REPORTS_BUCKET=$REPORTS_BUCKET,DATASETS_BUCKET=$DATASETS_BUCKET}' \\"
    echo "  --region $REGION"
    exit 1
fi

# Verify S3 buckets exist
echo "🪣 Verifying S3 buckets..."
if aws s3 ls "s3://$REPORTS_BUCKET" >/dev/null 2>&1; then
    echo "  ✅ Reports bucket ($REPORTS_BUCKET) exists"
else
    echo "  ❌ Reports bucket ($REPORTS_BUCKET) not found!"
    echo "  Creating bucket..."
    aws s3 mb "s3://$REPORTS_BUCKET" --region $REGION
    echo "  ✅ Reports bucket created"
fi

if aws s3 ls "s3://$DATASETS_BUCKET" >/dev/null 2>&1; then
    echo "  ✅ Datasets bucket ($DATASETS_BUCKET) exists"
else
    echo "  ⚠️ Datasets bucket ($DATASETS_BUCKET) not found!"
    echo "  This bucket should be used for data files, not Python reports."
fi

# Clean up
rm -rf lambda-package lambda-deployment.zip

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "📝 Summary of changes:"
echo "  1. Lambda function now uploads Python files to: s3://$REPORTS_BUCKET"
echo "  2. S3 key structure: {report_id}/main.py (e.g., dataiesb-reports/5/main.py)"
echo "  3. Added soft delete functionality (reports are marked as deleted, not removed)"
echo "  4. Added restore functionality for soft-deleted reports"
echo "  5. Removed duplicate 'Tipo de Gerenciamento' fields from admin interface"
echo "  6. Added separate tabs for active and deleted reports"
echo ""
echo "🔧 Next steps:"
echo "  1. Update your admin.html file with the new version from ../tmp/admin.html"
echo "  2. Test the upload functionality to ensure files go to the correct bucket"
echo "  3. Test the soft delete and restore functionality"
echo ""
echo "🚨 Important notes:"
echo "  - Python report files will now be stored in s3://$REPORTS_BUCKET"
echo "  - Data files should continue to use s3://$DATASETS_BUCKET"
echo "  - Soft delete allows users to hide/restore reports without permanent deletion"
