#!/bin/bash

# LinkedIn Functionality Demonstration Script
# This script shows how the LinkedIn integration works

echo "🔗 LinkedIn Profile Integration Demo - Data IESB Team"
echo "=================================================="
echo ""

echo "📋 Current Implementation:"
echo "1. Team data is stored in DynamoDB table 'DataIESB-Team'"
echo "2. Each team member can have an optional 'linkedin' field"
echo "3. The quem-somos.html page loads team data dynamically"
echo "4. LinkedIn buttons appear ONLY for members with profiles"
echo ""

echo "👀 How Users See LinkedIn Profiles:"
echo "1. Visit the quem-somos.html page"
echo "2. Look at the 'Equipe Técnica' section"
echo "3. Team members WITH LinkedIn profiles show a blue LinkedIn button"
echo "4. Team members WITHOUT LinkedIn profiles show no social links"
echo "5. Click the LinkedIn button to visit their profile (opens in new tab)"
echo ""

echo "🎯 Visual Indicators:"
echo "• LinkedIn button: Blue button with LinkedIn logo and text"
echo "• Hover effect: Button turns darker blue with animation"
echo "• Link icon (🔗) appears in top-right corner of member cards with LinkedIn"
echo ""

echo "📊 Current Team LinkedIn Status:"
echo "================================"

# Check if AWS CLI is available and configured
if command -v aws &> /dev/null; then
    echo "Checking DynamoDB for current LinkedIn profiles..."
    
    # Try to scan the table
    if aws dynamodb describe-table --table-name DataIESB-Team --region us-east-1 &> /dev/null; then
        echo ""
        echo "✅ Members WITH LinkedIn profiles:"
        aws dynamodb scan \
            --table-name DataIESB-Team \
            --filter-expression "attribute_exists(linkedin) AND active = :active" \
            --expression-attribute-values '{":active":{"BOOL":true}}' \
            --projection-expression "id, #n, linkedin" \
            --expression-attribute-names '{"#n": "name"}' \
            --region us-east-1 \
            --output json 2>/dev/null | jq -r '.Items[]? | "  • " + .name.S + " → " + .linkedin.S' || echo "  (No members with LinkedIn profiles found)"
        
        echo ""
        echo "❌ Members WITHOUT LinkedIn profiles:"
        aws dynamodb scan \
            --table-name DataIESB-Team \
            --filter-expression "attribute_not_exists(linkedin) AND active = :active" \
            --expression-attribute-values '{":active":{"BOOL":true}}' \
            --projection-expression "id, #n" \
            --expression-attribute-names '{"#n": "name"}' \
            --region us-east-1 \
            --output json 2>/dev/null | jq -r '.Items[]? | "  • " + .name.S' || echo "  (All members have LinkedIn profiles)"
    else
        echo "⚠️  DynamoDB table not found or not accessible"
        echo "   Run './setup-team-table.sh' to create the table"
    fi
else
    echo "⚠️  AWS CLI not found or not configured"
    echo "   The page will use fallback static data"
fi

echo ""
echo "🛠️  How to Add LinkedIn Profiles:"
echo "================================"
echo "Method 1 - Using the management script:"
echo "  ./manage-linkedin.sh add [member_id] [linkedin_url]"
echo "  Example: ./manage-linkedin.sh add 3 https://www.linkedin.com/in/natalia-evangelista"
echo ""
echo "Method 2 - Using AWS CLI directly:"
echo "  aws dynamodb update-item --table-name DataIESB-Team \\"
echo "    --key '{\"id\":{\"S\":\"3\"}}' \\"
echo "    --update-expression 'SET linkedin = :url, updatedAt = :time' \\"
echo "    --expression-attribute-values '{\\":url\\":{\\"S\\":\\"https://linkedin.com/in/profile\\"},\\":time\\":{\\"S\\":\\"$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)\\"}}'"
echo ""

echo "🌐 Testing the Functionality:"
echo "============================"
echo "1. Open test-linkedin.html in your browser to see examples"
echo "2. Open quem-somos.html to see the live implementation"
echo "3. Look for the blue LinkedIn buttons under team member information"
echo "4. Click any LinkedIn button to visit the profile"
echo ""

echo "📁 Files involved in LinkedIn functionality:"
echo "• quem-somos.html - Main page with team section"
echo "• js/team-data.js - JavaScript that loads data and renders LinkedIn links"
echo "• style/team-dynamic.css - Styling for LinkedIn buttons"
echo "• setup-team-table.sh - Script to create DynamoDB table"
echo "• manage-linkedin.sh - Script to manage LinkedIn profiles"
echo "• test-linkedin.html - Demo page showing how it works"
echo ""

echo "✨ The LinkedIn buttons will appear automatically when:"
echo "1. Team member has a 'linkedin' field in the database"
echo "2. The field contains a valid URL"
echo "3. The team member is marked as 'active: true'"
echo ""

echo "Demo completed! Visit quem-somos.html to see the LinkedIn integration in action."
