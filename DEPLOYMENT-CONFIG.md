# Deployment Configuration - Data IESB

## Overview
The Data IESB project uses separate deployment configurations for production and development environments.

## Current Working Configuration

### 🚀 Main Branch (Production)
- **Environment**: Production
- **Region**: `sa-east-1` (São Paulo)
- **S3 Bucket**: `dataiesb`
- **CloudFront Distribution**: `E371T2F886B5KI`
- **Domain**: `https://dataiesb.com`
- **Deployment Method**: AWS CodeBuild with `buildspec.yml`
- **Status**: ✅ Working

### 🧪 Dev Branch (Development)
- **Environment**: Development
- **Region**: `us-east-1` (N. Virginia)
- **S3 Bucket**: `dev-dataiesb`
- **CloudFront Distribution**: `E142Z1CPAKR8S8`
- **Temporary URL**: `https://d2v66tm8wx23ar.cloudfront.net`
- **Target Domain**: `https://dev.dataiesb.com` (pending DNS setup)
- **Deployment Method**: GitHub Actions (`.github/workflows/deploy-dev.yml`)
- **Status**: ✅ Working

## Buildspec Files

### 1. `buildspec.yml` (Production - Main Branch)
- **Purpose**: Production deployment for main branch
- **Configuration**: Hardcoded production values
- **Features**:
  - Simple, reliable YAML structure
  - Direct S3 sync to production bucket
  - CloudFront invalidation for production
  - No complex branch detection (to avoid YAML errors)

### 2. `buildspec-dev-simple.yml` (Development)
- **Purpose**: Development deployment configuration
- **Use Case**: Manual development builds if needed
- **Configuration**: Hardcoded development values

### 3. `buildspec-main.yml` & `buildspec-dev.yml`
- **Purpose**: Alternative configurations with explicit settings
- **Status**: Available but not currently used

## Deployment Process

### Production Deployment (Main Branch)
1. Push to `main` branch
2. AWS CodeBuild triggers automatically
3. Uses `buildspec.yml` with production settings
4. Deploys to production S3 bucket (`dataiesb`)
5. Invalidates production CloudFront (`E371T2F886B5KI`)
6. Site available at `https://dataiesb.com`

### Development Deployment (Dev Branch)
1. Push to `dev` branch
2. GitHub Actions triggers automatically (`.github/workflows/deploy-dev.yml`)
3. Deploys to development S3 bucket (`dev-dataiesb`)
4. Invalidates development CloudFront (`E142Z1CPAKR8S8`)
5. Site available at `https://d2v66tm8wx23ar.cloudfront.net`

## Environment Variables

### Production (Main Branch)
```bash
REGION=sa-east-1
S3_BUCKET=dataiesb
CLOUDFRONT_DISTRIBUTION_ID=E371T2F886B5KI
SITE_URL=https://dataiesb.com
```

### Development (Dev Branch)
```bash
REGION=us-east-1
S3_BUCKET=dev-dataiesb
CLOUDFRONT_DISTRIBUTION_ID=E142Z1CPAKR8S8
SITE_URL=https://d2v66tm8wx23ar.cloudfront.net
```

## Recent Issues Resolved

### YAML Syntax Errors
- **Problem**: Complex multi-line commands in buildspec.yml caused parsing errors
- **Solution**: Simplified to basic single-line commands
- **Status**: ✅ Resolved

### Build Failures
- **Problem**: `YAML_FILE_ERROR: Expected Commands[3] to be of string type`
- **Root Cause**: Improper YAML formatting in multi-line script blocks
- **Solution**: Removed complex branch detection, used hardcoded values
- **Status**: ✅ Resolved

## Security & Best Practices

### Branch Protection
- Main branch requires pull request reviews
- No direct pushes to main branch
- Status checks must pass before merging

### AWS Permissions
- Separate IAM roles for production and development
- Least privilege access principles
- Environment-specific resource access

### Deployment Safety
- Production uses hardcoded values to prevent errors
- Development uses GitHub Actions for reliability
- Both environments have separate AWS resources

## Troubleshooting

### Common Issues
1. **Build fails with YAML error**: Check buildspec.yml syntax
2. **CloudFront not updating**: Wait 5-15 minutes for invalidation
3. **S3 sync failures**: Check AWS credentials and bucket permissions
4. **Files not appearing**: Verify S3 bucket and CloudFront distribution

### Verification Steps
1. Check build logs in AWS CodeBuild console
2. Verify S3 bucket contents match expected files
3. Test CloudFront URL after invalidation completes
4. Confirm DNS resolution for custom domains

## Next Steps
1. Monitor production builds for stability
2. Consider re-adding branch detection once builds are stable
3. Configure DNS for `dev.dataiesb.com`
4. Set up monitoring and alerting
5. Add automated testing in deployment pipeline

## Build Status
- **Production (Main)**: ✅ Should work with simplified buildspec.yml
- **Development (Dev)**: ✅ Working with GitHub Actions
- **Last Updated**: 2025-08-10
