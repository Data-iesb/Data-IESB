#!/bin/bash

# Automated script to set up auth.dataiesb.com custom domain for Cognito
# This will monitor the certificate and set up the custom domain when ready

CERTIFICATE_ARN="arn:aws:acm:us-east-1:248189947068:certificate/5d059468-405e-4d10-8eb5-c6051848721d"
USER_POOL_ID="us-east-1_QvLQs82bE"
CUSTOM_DOMAIN="auth.dataiesb.com"
CURRENT_DOMAIN="us-east-1qvlqs82be"
HOSTED_ZONE_ID="Z05014761ROYBA3Z5YKY2"

echo "🔍 Monitoring certificate validation for auth.dataiesb.com..."
echo "Certificate ARN: $CERTIFICATE_ARN"
echo ""

# Function to check certificate status
check_certificate() {
    aws acm describe-certificate --certificate-arn $CERTIFICATE_ARN --region us-east-1 --query 'Certificate.Status' --output text 2>/dev/null
}

# Function to set up custom domain
setup_custom_domain() {
    echo "✅ Certificate validated! Setting up custom domain..."
    
    # Delete current domain
    echo "🗑️  Deleting current Cognito domain..."
    aws cognito-idp delete-user-pool-domain --user-pool-id $USER_POOL_ID --domain $CURRENT_DOMAIN --region us-east-1
    
    # Wait for deletion
    sleep 15
    
    # Create custom domain
    echo "🚀 Creating custom domain: $CUSTOM_DOMAIN"
    RESULT=$(aws cognito-idp create-user-pool-domain \
        --user-pool-id $USER_POOL_ID \
        --domain $CUSTOM_DOMAIN \
        --custom-domain-config CertificateArn=$CERTIFICATE_ARN \
        --region us-east-1 2>&1)
    
    if [ $? -eq 0 ]; then
        echo "✅ Custom domain created successfully!"
        
        # Get CloudFront distribution
        echo "📡 Getting CloudFront distribution..."
        CLOUDFRONT_DOMAIN=$(aws cognito-idp describe-user-pool-domain --domain $CUSTOM_DOMAIN --region us-east-1 --query 'DomainDescription.CloudFrontDistribution' --output text)
        
        if [ "$CLOUDFRONT_DOMAIN" != "None" ] && [ "$CLOUDFRONT_DOMAIN" != "" ]; then
            echo "🌐 CloudFront Distribution: $CLOUDFRONT_DOMAIN"
            
            # Update Route53 record to point to CloudFront
            echo "🔄 Updating Route53 record to point to CloudFront..."
            aws route53 change-resource-record-sets \
                --hosted-zone-id $HOSTED_ZONE_ID \
                --change-batch "{
                    \"Changes\": [{
                        \"Action\": \"UPSERT\",
                        \"ResourceRecordSet\": {
                            \"Name\": \"$CUSTOM_DOMAIN\",
                            \"Type\": \"CNAME\",
                            \"TTL\": 300,
                            \"ResourceRecords\": [{\"Value\": \"$CLOUDFRONT_DOMAIN\"}]
                        }
                    }]
                }" > /dev/null
            
            echo "✅ DNS updated! auth.dataiesb.com now points to CloudFront"
            echo ""
            echo "🎉 Setup complete! Your custom domain is ready:"
            echo "   https://auth.dataiesb.com/signup?client_id=87slk0n2malm3h7rv8p10jfak&redirect_uri=https%3A%2F%2Fdataiesb.com&response_type=code&scope=email+openid+phone"
            echo ""
            echo "⏰ DNS propagation may take 5-15 minutes to complete globally."
        else
            echo "❌ Could not get CloudFront distribution"
        fi
    else
        echo "❌ Failed to create custom domain: $RESULT"
        # Recreate original domain
        echo "🔄 Recreating original domain..."
        aws cognito-idp create-user-pool-domain --user-pool-id $USER_POOL_ID --domain $CURRENT_DOMAIN --region us-east-1 > /dev/null
    fi
}

# Monitor certificate status
MAX_ATTEMPTS=30
ATTEMPT=1

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    STATUS=$(check_certificate)
    
    if [ "$STATUS" = "ISSUED" ]; then
        setup_custom_domain
        exit 0
    elif [ "$STATUS" = "FAILED" ] || [ "$STATUS" = "VALIDATION_TIMED_OUT" ]; then
        echo "❌ Certificate validation failed: $STATUS"
        exit 1
    else
        echo "⏳ Attempt $ATTEMPT/$MAX_ATTEMPTS - Certificate status: $STATUS"
        sleep 30
        ATTEMPT=$((ATTEMPT + 1))
    fi
done

echo "⏰ Certificate validation is taking longer than expected."
echo "   You can run this script again later or check manually:"
echo "   aws acm describe-certificate --certificate-arn $CERTIFICATE_ARN --region us-east-1"
