# 🚨 Google OAuth Error Fix Guide

## Error: "Access blocked: This app's request is invalid"

### ✅ What I've Already Fixed:
1. **Updated Cognito Google Identity Provider** - Changed scopes from `email` to `email openid profile`
2. **Added proper attribute mapping** - Now includes name, given_name, family_name, picture
3. **Updated User Pool Client** - Added Google to supported identity providers

### 🔧 What You Need to Fix in Google Console:

#### 1. Go to Google Cloud Console
Visit: https://console.developers.google.com/apis/credentials

#### 2. Find Your OAuth 2.0 Client
Look for: `781293193566-s1e99d7eiqgdlgcudevuf8hjjre2ssrp.apps.googleusercontent.com`

#### 3. Update Authorized JavaScript Origins
Add these EXACT URLs:
```
https://auth.dataiesb.com
https://dataiesb.com  
https://www.dataiesb.com
http://localhost:8000
```

#### 4. Update Authorized Redirect URIs
Add this EXACT URL:
```
https://auth.dataiesb.com/oauth2/idpresponse
```

#### 5. OAuth Consent Screen
- Go to "OAuth consent screen" in the left menu
- Make sure the app is set to "In production" (not "Testing")
- Add `dataiesb.com` to authorized domains
- Fill out all required fields

### 🧪 Testing Steps:

1. **Use the diagnostic page**: Open `google-oauth-diagnostic.html`
2. **Try simple test**: Open `login-simple-test.html` 
3. **Test with minimal scopes**: Start with "email only" test
4. **Gradually add scopes**: If email works, try "email openid", then full scopes

### 📋 Common Issues & Solutions:

| Issue | Solution |
|-------|----------|
| "redirect_uri_mismatch" | Check redirect URI is exactly `https://auth.dataiesb.com/oauth2/idpresponse` |
| "invalid_client" | Verify Google Client ID matches in both Google Console and Cognito |
| "access_blocked" | Change app from "Testing" to "Production" in Google Console |
| "unauthorized_client" | Add all required JavaScript origins |

### 🔄 Propagation Time:
- Google Console changes can take 5-10 minutes to propagate
- Try clearing browser cache if issues persist

### 🆘 If Still Not Working:

1. **Check Google Console Logs**: Look for specific error messages
2. **Try Direct Google OAuth**: Use the diagnostic page to test Google OAuth directly
3. **Verify Domain Ownership**: Make sure `dataiesb.com` is verified in Google Console
4. **Check Quotas**: Ensure you haven't exceeded Google OAuth quotas

### 📞 Quick Test Commands:

```bash
# Test the diagnostic page
open http://localhost:8000/google-oauth-diagnostic.html

# Test simple login
open http://localhost:8000/login-simple-test.html

# Check current configuration
curl -s https://auth.dataiesb.com/.well-known/openid_configuration | jq
```

### 🎯 Expected Working Flow:

1. User clicks "Entrar com Gmail IESB"
2. Redirects to `https://auth.dataiesb.com/oauth2/authorize?...`
3. Cognito redirects to Google OAuth
4. User authenticates with Google
5. Google redirects to `https://auth.dataiesb.com/oauth2/idpresponse`
6. Cognito processes and redirects to your callback URL
7. Your app exchanges code for tokens

The most likely fix is updating the Google Console configuration with the correct redirect URI and changing the app status from "Testing" to "Production".
