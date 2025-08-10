#!/bin/bash

# Amazon Q Business Chatbot Setup Script
# This script helps you set up and configure the Q Business chatbot integration

set -e

echo "🚀 Amazon Q Business Chatbot Setup"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    echo "Please install pip3 and try again."
    exit 1
fi

echo "✅ Python 3 and pip3 are available"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo ""
    echo "⚠️  AWS CLI is not installed."
    echo "You'll need to install and configure AWS CLI to use Amazon Q Business."
    echo "Visit: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
else
    echo "✅ AWS CLI is available"
    
    # Check AWS configuration
    if aws sts get-caller-identity &> /dev/null; then
        echo "✅ AWS credentials are configured"
        ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
        REGION=$(aws configure get region || echo "us-east-1")
        echo "   Account ID: $ACCOUNT_ID"
        echo "   Region: $REGION"
    else
        echo "⚠️  AWS credentials are not configured"
        echo "Run 'aws configure' to set up your credentials"
    fi
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env configuration file..."
    cp .env.template .env
    echo "✅ Created .env file from template"
    echo "⚠️  Please edit .env file and add your Q Business Application ID"
else
    echo "✅ .env file already exists"
fi

# Check if Q Business Application ID is configured
if [ -f .env ]; then
    if grep -q "your-q-business-application-id-here" .env; then
        echo ""
        echo "⚠️  Q Business Application ID not configured in .env file"
        echo "Please edit .env and replace 'your-q-business-application-id-here' with your actual Application ID"
    else
        echo "✅ Q Business Application ID appears to be configured"
    fi
fi

echo ""
echo "🔧 Setup Instructions:"
echo "====================="
echo ""
echo "1. Configure Amazon Q Business:"
echo "   - Go to AWS Console > Amazon Q Business"
echo "   - Create or select your Q Business application"
echo "   - Copy the Application ID"
echo "   - Update the Q_BUSINESS_APPLICATION_ID in .env file"
echo ""
echo "2. Add knowledge sources to your Q Business application:"
echo "   - Upload documents about your partners"
echo "   - Configure data sources (S3, SharePoint, etc.)"
echo "   - Wait for indexing to complete"
echo ""
echo "3. Start the chatbot server:"
echo "   ./start-chatbot.sh"
echo ""
echo "4. Open your web page (parceiros.html) in a browser"
echo "   The chatbot widget will appear in the bottom-right corner"
echo ""

# Create start script
echo "📝 Creating start script..."
cat > start-chatbot.sh << 'EOF'
#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "🚀 Starting Amazon Q Business Chatbot Server..."
echo "Server will be available at: http://localhost:${PORT:-5000}"
echo "Press Ctrl+C to stop the server"
echo ""

python3 chatbot_backend.py
EOF

chmod +x start-chatbot.sh

echo "✅ Created start-chatbot.sh script"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Q Business Application ID"
echo "2. Run: ./start-chatbot.sh"
echo "3. Open parceiros.html in your browser"
echo ""
echo "For help with Amazon Q Business setup, visit:"
echo "https://docs.aws.amazon.com/amazonq/latest/business-use-dg/"
