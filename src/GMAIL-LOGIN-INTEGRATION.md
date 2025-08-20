# Gmail Login Integration - Data IESB

## 📋 Overview

This document describes the Gmail login integration added to the Data IESB platform using Amazon Cognito User Pool with Google as an Identity Provider.

## 🔧 Configuration

### Cognito User Pool Settings
- **User Pool ID**: `us-east-1_QvLQs82bE`
- **User Pool Name**: `User pool - b0p3ui`
- **Client ID**: `71am2v0jcp9uqpihrh9hjqtp6o`
- **Client Name**: `dataiesb-web-app`
- **Custom Domain**: `auth.dataiesb.com`

### Google Identity Provider
- **Provider Type**: Google
- **Client ID**: `781293193566-s1e99d7eiqgdlgcudevuf8hjjre2ssrp.apps.googleusercontent.com`
- **Status**: ✅ Configured and Active

### OAuth Configuration
- **Allowed OAuth Flows**: Authorization Code Grant
- **Allowed OAuth Scopes**: `email`, `openid`, `profile`
- **Callback URLs**:
  - `http://localhost:8000/admin.html`
  - `http://localhost:8000/callback.html`
  - `https://dataiesb.com/admin.html`
  - `https://dataiesb.com/callback.html`
  - `https://www.dataiesb.com/admin.html`
  - `https://www.dataiesb.com/callback.html`
- **Logout URLs**:
  - `http://localhost:8000/index.html`
  - `https://dataiesb.com/index.html`
  - `https://www.dataiesb.com/index.html`

## 📁 Files Modified/Created

### Modified Files
1. **`login.html`** - Enhanced with Gmail login button and OAuth handling
2. **`admin.html`** - Updated authentication to handle OAuth tokens

### New Files
1. **`callback.html`** - OAuth callback handler for processing authentication
2. **`test-gmail-login.html`** - Test page for verifying Gmail integration
3. **`GMAIL-LOGIN-INTEGRATION.md`** - This documentation file

## 🚀 How It Works

### 1. User Flow
1. User visits `login.html`
2. User clicks "Entrar com Gmail IESB" button
3. User is redirected to Cognito hosted UI with Google OAuth
4. User authenticates with their Google account
5. Google redirects back to `callback.html` with authorization code
6. `callback.html` exchanges code for tokens and validates IESB email domain
7. User is redirected to `admin.html` with stored tokens

### 2. Authentication Process
```javascript
// OAuth URL Construction
const params = new URLSearchParams({
    client_id: '71am2v0jcp9uqpihrh9hjqtp6o',
    response_type: 'code',
    scope: 'email openid profile',
    redirect_uri: window.location.origin + '/callback.html',
    identity_provider: 'Google'
});

const googleUrl = `https://auth.dataiesb.com/oauth2/authorize?${params.toString()}`;
```

### 3. Token Management
The system stores the following tokens in localStorage:
- `accessToken` - OAuth access token
- `idToken` - JWT ID token for API authentication
- `refreshToken` - Token for refreshing access
- `userInfo` - User profile information from Google

### 4. Email Domain Validation
The system validates that users have `@iesb.edu.br` email addresses:
```javascript
function validateIESBEmail(email) {
    return email && email.endsWith('@iesb.edu.br');
}
```

## 🔒 Security Features

### 1. Domain Restriction
- Only `@iesb.edu.br` email addresses are allowed
- Validation occurs both in frontend and during OAuth callback

### 2. Token Security
- Tokens are stored in localStorage (consider upgrading to httpOnly cookies for production)
- ID tokens are used for API authentication
- Automatic logout on token validation failures

### 3. HTTPS Enforcement
- All OAuth flows require HTTPS in production
- Callback URLs are configured for both development and production environments

## 🧪 Testing

### Test Page
Use `test-gmail-login.html` to verify the integration:
1. Check authentication status
2. View stored tokens
3. Test Google login flow
4. Clear tokens for testing

### Manual Testing Steps
1. Open `login.html`
2. Click "Entrar com Gmail IESB"
3. Sign in with an `@iesb.edu.br` Google account
4. Verify redirection to `admin.html`
5. Confirm user information is displayed correctly

## 🔧 Configuration URLs

### Cognito Hosted UI URLs
- **Login**: `https://auth.dataiesb.com/oauth2/authorize`
- **Token Exchange**: `https://auth.dataiesb.com/oauth2/token`
- **User Info**: `https://auth.dataiesb.com/oauth2/userInfo`
- **Logout**: `https://auth.dataiesb.com/logout`

### Google OAuth Configuration
Ensure your Google OAuth application has these settings:
- **Authorized JavaScript origins**: 
  - `https://dataiesb.com`
  - `https://www.dataiesb.com`
  - `http://localhost:8000` (for development)
- **Authorized redirect URIs**:
  - `https://auth.dataiesb.com/oauth2/idpresponse`

## 🐛 Troubleshooting

### Common Issues

1. **"Access Denied" Error**
   - Verify email domain is `@iesb.edu.br`
   - Check Google OAuth configuration

2. **"Invalid Redirect URI" Error**
   - Verify callback URLs in Cognito User Pool Client
   - Check Google OAuth authorized redirect URIs

3. **Token Validation Errors**
   - Clear localStorage tokens
   - Verify Cognito configuration
   - Check network connectivity

### Debug Steps
1. Open browser developer tools
2. Check console for error messages
3. Verify network requests in Network tab
4. Use `test-gmail-login.html` for detailed debugging

## 📊 Monitoring

### CloudWatch Logs
Monitor these Cognito events:
- Sign-in attempts
- Token exchanges
- Authentication failures

### Application Logs
The frontend logs authentication events to the browser console:
- OAuth redirects
- Token storage/retrieval
- Authentication status changes

## 🔄 Maintenance

### Token Refresh
Currently, the system doesn't implement automatic token refresh. Consider adding:
```javascript
async function refreshTokens() {
    const refreshToken = localStorage.getItem('refreshToken');
    // Implement token refresh logic
}
```

### Regular Tasks
1. Monitor Cognito usage and costs
2. Review authentication logs for suspicious activity
3. Update Google OAuth credentials as needed
4. Test authentication flow after any infrastructure changes

## 📞 Support

For issues with the Gmail integration:
1. Check this documentation
2. Use the test page for debugging
3. Review Cognito CloudWatch logs
4. Verify Google OAuth configuration

## 🎯 Future Enhancements

1. **Automatic Token Refresh**: Implement refresh token logic
2. **Session Management**: Add proper session timeout handling
3. **Multi-Factor Authentication**: Consider adding MFA for enhanced security
4. **Audit Logging**: Implement comprehensive authentication audit logs
5. **Mobile Support**: Optimize OAuth flow for mobile devices
