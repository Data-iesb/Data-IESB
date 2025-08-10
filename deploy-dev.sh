#!/bin/bash

# Data IESB Development Deployment Script
# This script deploys the dev branch to dev.dataiesb.com infrastructure

set -e

echo "🚀 Starting Data IESB Development Deployment..."

# Check if we're on dev branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "dev" ]; then
    echo "❌ Error: You must be on the 'dev' branch to deploy to development environment"
    echo "Current branch: $CURRENT_BRANCH"
    echo "Run: git checkout dev"
    exit 1
fi

# Configuration
DEV_BUCKET="dev-dataiesb"
CLOUDFRONT_DISTRIBUTION_ID="E142Z1CPAKR8S8"
SOURCE_DIR="src/"

echo "📋 Deployment Configuration:"
echo "   Branch: $CURRENT_BRANCH"
echo "   S3 Bucket: $DEV_BUCKET"
echo "   CloudFront Distribution: $CLOUDFRONT_DISTRIBUTION_ID"
echo "   Source Directory: $SOURCE_DIR"
echo ""

# Sync files to S3
echo "📁 Syncing files to S3 bucket..."
aws s3 sync $SOURCE_DIR s3://$DEV_BUCKET/ --delete --exclude "*.sh" --exclude "*.json" --exclude ".git/*"

if [ $? -eq 0 ]; then
    echo "✅ Files successfully synced to S3"
else
    echo "❌ Error syncing files to S3"
    exit 1
fi

# Invalidate CloudFront cache
echo "🔄 Invalidating CloudFront cache..."
INVALIDATION_ID=$(aws cloudfront create-invalidation \
    --distribution-id $CLOUDFRONT_DISTRIBUTION_ID \
    --paths "/*" \
    --query 'Invalidation.Id' \
    --output text)

if [ $? -eq 0 ]; then
    echo "✅ CloudFront invalidation created: $INVALIDATION_ID"
    echo "🌐 Development site will be available at:"
    echo "   CloudFront URL: https://d2v66tm8wx23ar.cloudfront.net"
    echo "   S3 Website URL: http://dev-dataiesb.s3-website-us-east-1.amazonaws.com"
else
    echo "❌ Error creating CloudFront invalidation"
    exit 1
fi

echo ""
echo "🎉 Development deployment completed successfully!"
echo "📝 Next steps:"
echo "   1. Wait 5-15 minutes for CloudFront distribution to update"
echo "   2. Configure DNS for dev.dataiesb.com to point to CloudFront"
echo "   3. Set up SSL certificate for custom domain"
echo ""
