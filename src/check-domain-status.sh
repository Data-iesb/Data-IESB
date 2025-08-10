#!/bin/bash

# Script to monitor when auth.dataiesb.com becomes active

CUSTOM_DOMAIN="auth.dataiesb.com"

echo "🔍 Monitoring Cognito custom domain status..."
echo "Domain: $CUSTOM_DOMAIN"
echo ""

check_status() {
    aws cognito-idp describe-user-pool-domain --domain $CUSTOM_DOMAIN --region us-east-1 --query 'DomainDescription.Status' --output text 2>/dev/null
}

test_url() {
    curl -s -o /dev/null -w "%{http_code}" "https://$CUSTOM_DOMAIN/signup?client_id=87slk0n2malm3h7rv8p10jfak&redirect_uri=https%3A%2F%2Fdataiesb.com&response_type=code&scope=email+openid+phone" 2>/dev/null
}

MAX_ATTEMPTS=20
ATTEMPT=1

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    STATUS=$(check_status)
    HTTP_CODE=$(test_url)
    
    echo "⏳ Attempt $ATTEMPT/$MAX_ATTEMPTS"
    echo "   Status: $STATUS"
    echo "   HTTP Response: $HTTP_CODE"
    
    if [ "$STATUS" = "ACTIVE" ] && [ "$HTTP_CODE" = "200" ]; then
        echo ""
        echo "🎉 SUCCESS! Custom domain is now active and working!"
        echo "✅ https://auth.dataiesb.com is ready to use"
        echo ""
        echo "🔗 Test URL:"
        echo "https://auth.dataiesb.com/signup?client_id=87slk0n2malm3h7rv8p10jfak&redirect_uri=https%3A%2F%2Fdataiesb.com&response_type=code&scope=email+openid+phone"
        exit 0
    elif [ "$STATUS" = "FAILED" ]; then
        echo "❌ Domain setup failed!"
        exit 1
    else
        echo "   ⏰ Still setting up... waiting 30 seconds"
        sleep 30
        ATTEMPT=$((ATTEMPT + 1))
    fi
    echo ""
done

echo "⏰ Domain is taking longer than expected to become active."
echo "Current status: $(check_status)"
echo "You can check manually with:"
echo "aws cognito-idp describe-user-pool-domain --domain $CUSTOM_DOMAIN --region us-east-1"
