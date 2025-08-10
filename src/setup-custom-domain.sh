#!/bin/bash

# Script to set up custom Cognito domain for auth.dataiesb.com
# Run this after adding the DNS validation record

CERTIFICATE_ARN="arn:aws:acm:us-east-1:248189947068:certificate/5d059468-405e-4d10-8eb5-c6051848721d"
USER_POOL_ID="us-east-1_QvLQs82bE"
CUSTOM_DOMAIN="auth.dataiesb.com"
CURRENT_DOMAIN="us-east-1qvlqs82be"

echo "Checking certificate validation status..."

# Check certificate status
CERT_STATUS=$(aws acm describe-certificate --certificate-arn $CERTIFICATE_ARN --region us-east-1 --query 'Certificate.Status' --output text)

if [ "$CERT_STATUS" = "ISSUED" ]; then
    echo "✅ Certificate is validated! Setting up custom domain..."
    
    # Delete current domain
    echo "Deleting current Cognito domain..."
    aws cognito-idp delete-user-pool-domain --domain $CURRENT_DOMAIN --region us-east-1
    
    # Wait a bit for deletion to complete
    sleep 10
    
    # Create custom domain
    echo "Creating custom domain: $CUSTOM_DOMAIN"
    aws cognito-idp create-user-pool-domain \
        --user-pool-id $USER_POOL_ID \
        --domain $CUSTOM_DOMAIN \
        --custom-domain-config CertificateArn=$CERTIFICATE_ARN \
        --region us-east-1
    
    # Get the CloudFront distribution for DNS setup
    echo "Getting CloudFront distribution for DNS setup..."
    aws cognito-idp describe-user-pool-domain --domain $CUSTOM_DOMAIN --region us-east-1
    
    echo ""
    echo "🎉 Custom domain setup initiated!"
    echo "Next steps:"
    echo "1. Add CNAME record: auth.dataiesb.com -> [CloudFront distribution from above]"
    echo "2. Update your HTML to use: https://auth.dataiesb.com/signup?..."
    
else
    echo "❌ Certificate status: $CERT_STATUS"
    echo "Please add the DNS validation record first:"
    echo ""
    echo "DNS Record:"
    echo "Type: CNAME"
    echo "Name: _e0ab98d598c0c26c856d9bdbb6a945f5.auth.dataiesb.com"
    echo "Value: _f636ca2e30a2e7b7f528c54418307e3e.xlfgrmvvlj.acm-validations.aws"
    echo ""
    echo "Then run this script again in a few minutes."
fi
