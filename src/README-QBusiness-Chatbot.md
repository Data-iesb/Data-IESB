# Amazon Q Business Chatbot Integration

This project integrates an Amazon Q Business chatbot into your Data IESB website to provide intelligent responses about your partners and knowledge base.

## 🚀 Quick Start

1. **Run the setup script:**
   ```bash
   ./setup-qbusiness-chatbot.sh
   ```

2. **Configure your environment:**
   - Edit `.env` file with your Q Business Application ID
   - Ensure AWS credentials are configured

3. **Start the chatbot server:**
   ```bash
   ./start-chatbot.sh
   ```

4. **Open your website:**
   - Navigate to `parceiros.html` in your browser
   - The chatbot widget will appear in the bottom-right corner

## 📋 Prerequisites

- Python 3.7+
- AWS CLI configured with appropriate permissions
- Amazon Q Business application set up in AWS
- Knowledge sources configured in Q Business

## 🔧 Configuration

### Environment Variables (.env file)

```bash
# Required
Q_BUSINESS_APPLICATION_ID=your-application-id-here

# Optional
Q_BUSINESS_USER_ID=default-user
AWS_REGION=us-east-1
FLASK_DEBUG=False
PORT=5000
```

### AWS Permissions

Your AWS credentials need the following permissions:
- `qbusiness:Chat`
- `qbusiness:ChatSync`
- Access to your specific Q Business application

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │  Flask Backend  │    │ Amazon Q Business│
│  (parceiros.html)│◄──►│ (chatbot_backend)│◄──►│   Application   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Components

1. **Frontend Widget** (`js/qbusiness-chatbot.js`)
   - Embeddable JavaScript chatbot widget
   - Customizable appearance and behavior
   - Responsive design

2. **Backend API** (`chatbot_backend.py`)
   - Flask server handling chat requests
   - Amazon Q Business integration
   - CORS enabled for cross-origin requests

3. **Configuration**
   - Environment-based configuration
   - AWS credentials management
   - Customizable chatbot settings

## 🎨 Customization

### Chatbot Appearance

Edit the configuration in `parceiros.html`:

```javascript
window.qbChatbotConfig = {
    title: 'Your Custom Title',
    welcomeMessage: 'Your welcome message',
    placeholder: 'Your input placeholder...',
    primaryColor: '#your-primary-color',
    accentColor: '#your-accent-color',
    position: 'bottom-right' // or 'bottom-left', 'top-right', 'top-left'
};
```

### Adding to Other Pages

To add the chatbot to other HTML pages:

1. Include the JavaScript file:
   ```html
   <script src="./js/qbusiness-chatbot.js"></script>
   ```

2. Configure and initialize:
   ```html
   <script>
   window.qbChatbotConfig = {
       apiUrl: 'http://localhost:5000',
       title: 'Your Assistant',
       // ... other options
   };
   
   document.addEventListener('DOMContentLoaded', function() {
       new QBusinessChatbot(window.qbChatbotConfig);
   });
   </script>
   ```

## 🔍 Amazon Q Business Setup

### 1. Create Q Business Application

1. Go to AWS Console > Amazon Q Business
2. Click "Create application"
3. Choose your configuration:
   - **Identity Center**: For user management
   - **IAM Identity Center**: Recommended for enterprise
4. Note your Application ID

### 2. Add Knowledge Sources

Add relevant documents about your partners:

- **S3 Bucket**: Upload partner documents, PDFs, etc.
- **Web Crawler**: Crawl partner websites
- **SharePoint**: Connect to SharePoint sites
- **Confluence**: Connect to Confluence spaces

### 3. Configure Data Sources

1. In your Q Business application, go to "Data sources"
2. Add your preferred data source type
3. Configure connection settings
4. Start sync/crawling
5. Wait for indexing to complete

### 4. Test Your Application

1. Use the Q Business console to test queries
2. Ensure responses are relevant and accurate
3. Adjust data sources as needed

## 🚀 Deployment

### Development
```bash
# Start development server
./start-chatbot.sh
```

### Production

1. **Update API URL**: Change `apiUrl` in your HTML files to your production server
2. **Environment Variables**: Set production values in `.env`
3. **HTTPS**: Use HTTPS in production for security
4. **Process Manager**: Use PM2, systemd, or similar for process management

Example with PM2:
```bash
npm install -g pm2
pm2 start chatbot_backend.py --name qbusiness-chatbot --interpreter python3
```

## 🔒 Security Considerations

- **API Keys**: Never expose AWS credentials in frontend code
- **CORS**: Configure CORS appropriately for your domain
- **Rate Limiting**: Consider implementing rate limiting
- **Input Validation**: Backend validates all user inputs
- **HTTPS**: Use HTTPS in production

## 🐛 Troubleshooting

### Common Issues

1. **"Q Business not properly configured"**
   - Check your `.env` file
   - Verify Q_BUSINESS_APPLICATION_ID is correct
   - Ensure AWS credentials are configured

2. **"AWS credentials not found"**
   - Run `aws configure` to set up credentials
   - Or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables

3. **"Connection error"**
   - Ensure the Flask server is running
   - Check the API URL in your frontend configuration
   - Verify network connectivity

4. **Empty or irrelevant responses**
   - Check your Q Business data sources
   - Ensure documents are properly indexed
   - Test queries in the Q Business console

### Debug Mode

Enable debug mode for detailed logging:
```bash
export FLASK_DEBUG=True
./start-chatbot.sh
```

## 📚 API Reference

### POST /chat

Send a message to the chatbot.

**Request:**
```json
{
    "message": "Tell me about our partners",
    "conversationId": "optional-conversation-id"
}
```

**Response:**
```json
{
    "success": true,
    "response": "Here are our current partners...",
    "conversationId": "conversation-id-for-context",
    "sourceAttributions": [...]
}
```

### GET /widget

Returns the standalone chatbot widget HTML.

### GET /

Health check endpoint.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues related to:
- **Amazon Q Business**: Check AWS documentation
- **This integration**: Create an issue in this repository
- **AWS Setup**: Contact AWS Support

## 📖 Additional Resources

- [Amazon Q Business Documentation](https://docs.aws.amazon.com/amazonq/latest/business-use-dg/)
- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
