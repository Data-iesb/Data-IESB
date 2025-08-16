# Pipeline Trigger - Cognito Fix Deployment

**Trigger Date**: 2025-08-16 21:32 UTC
**Purpose**: Deploy Cognito signup integration fix to production
**Branch**: prod

## Changes Made:
- ✅ Fixed Cognito App Client OAuth flows
- ✅ Enabled `AllowedOAuthFlowsUserPoolClient: true`
- ✅ Signup URL now working: https://auth.dataiesb.com/signup
- ✅ Cadastrar page integration verified

## Expected Pipeline Behavior:
1. Detect `prod` branch
2. Deploy to production (sa-east-1)
3. Sync files to `dataiesb` S3 bucket
4. Invalidate CloudFront distribution
5. Update live site at https://dataiesb.com

## Verification After Deploy:
- Cognito signup flow working
- Users can register with @iesb.edu.br emails
- Redirect back to dataiesb.com after signup

**Status**: Ready for deployment
