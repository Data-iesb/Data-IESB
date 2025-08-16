# Pipeline Test V2

**Test Date**: 2025-08-16 21:23 UTC
**Purpose**: Test CodeBuild pipeline after fixing CloudWatch Logs permissions
**Branch**: prod
**Changes**: Fixed IAM permissions for sa-east-1 region

## Issues Fixed:
- ✅ DynamoDB records standardized with `is_deleted` field
- ✅ Lambda function filter expression fixed
- ✅ API now returns only 6 active reports
- ✅ Deleted reports (5, 6, 9) properly filtered out
- ✅ CodeBuild CloudWatch Logs permissions fixed for sa-east-1

## IAM Fix Applied:
- Created policy: `CodeBuildLogsPolicy-sa-east-1`
- Attached to role: `codebuild-dataiesb-relatorios`
- Permissions for: `/aws/codebuild/dataiesb-site-prod` log group

## Expected pipeline behavior:
1. Detect `prod` branch
2. Deploy to production environment (sa-east-1)
3. Create CloudWatch logs successfully
4. Sync files to `dataiesb` S3 bucket
5. Invalidate CloudFront distribution `E371T2F886B5KI`
6. Site available at https://dataiesb.com

## Test verification:
After pipeline completes, verify:
- Website shows only 6 reports
- Deleted reports are not visible
- API filtering works correctly
- Build logs are accessible in CloudWatch
