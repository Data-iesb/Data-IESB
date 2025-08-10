# Deployment Configuration - Data IESB

## Overview
The Data IESB project uses branch-specific deployment configurations to ensure proper separation between development and production environments.

## Branch Configuration

### 🚀 Main Branch (Production)
- **Environment**: Production
- **Region**: `sa-east-1` (São Paulo)
- **S3 Bucket**: `dataiesb`
- **CloudFront Distribution**: `E371T2F886B5KI`
- **Domain**: `https://dataiesb.com`
- **Deployment Method**: AWS CodeBuild with buildspec.yml

### 🧪 Dev Branch (Development)
- **Environment**: Development
- **Region**: `us-east-1` (N. Virginia)
- **S3 Bucket**: `dev-dataiesb`
- **CloudFront Distribution**: `E142Z1CPAKR8S8`
- **Temporary URL**: `https://d2v66tm8wx23ar.cloudfront.net`
- **Target Domain**: `https://dev.dataiesb.com` (pending DNS setup)
- **Deployment Method**: GitHub Actions + AWS CodeBuild

## Buildspec Files

### 1. `buildspec.yml` (Smart Branch Detection)
- **Purpose**: Automatically detects branch and deploys to appropriate environment
- **Features**:
  - Branch detection from CodeBuild environment variables
  - Environment-specific configuration
  - Proper error handling for unsupported branches
  - Detailed logging and deployment summaries

### 2. `buildspec-main.yml` (Production Only)
- **Purpose**: Explicit production deployment configuration
- **Use Case**: When you need to force production deployment

### 3. `buildspec-dev.yml` (Development Only)
- **Purpose**: Explicit development deployment configuration
- **Use Case**: When you need to force development deployment

## GitHub Actions

### `.github/workflows/deploy-dev.yml`
- **Trigger**: Push to `dev` branch
- **Purpose**: Automated development deployments
- **Features**:
  - Automatic S3 sync
  - CloudFront invalidation
  - Deployment summaries
  - Error handling

## Deployment Process

### Production Deployment (Main Branch)
1. Push to `main` branch
2. AWS CodeBuild triggers automatically
3. `buildspec.yml` detects main branch
4. Deploys to production S3 bucket (`dataiesb`)
5. Invalidates production CloudFront (`E371T2F886B5KI`)
6. Site available at `https://dataiesb.com`

### Development Deployment (Dev Branch)
1. Push to `dev` branch
2. GitHub Actions triggers automatically
3. Deploys to development S3 bucket (`dev-dataiesb`)
4. Invalidates development CloudFront (`E142Z1CPAKR8S8`)
5. Site available at `https://d2v66tm8wx23ar.cloudfront.net`

## Manual Deployment Scripts

### `deploy-dev.sh`
- **Purpose**: Manual development deployment
- **Usage**: `./deploy-dev.sh`
- **Requirements**: Must be on `dev` branch
- **Features**: Branch validation, deployment confirmation

## Environment Variables

### Production (Main Branch)
```bash
ENVIRONMENT=production
REGION=sa-east-1
S3_BUCKET=dataiesb
CLOUDFRONT_DISTRIBUTION_ID=E371T2F886B5KI
SITE_URL=https://dataiesb.com
```

### Development (Dev Branch)
```bash
ENVIRONMENT=development
REGION=us-east-1
S3_BUCKET=dev-dataiesb
CLOUDFRONT_DISTRIBUTION_ID=E142Z1CPAKR8S8
SITE_URL=https://d2v66tm8wx23ar.cloudfront.net
```

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
- Automatic branch detection prevents wrong environment deployments
- Explicit logging of deployment targets
- Rollback capabilities through S3 versioning

## Troubleshooting

### Common Issues
1. **Wrong environment deployment**: Check branch name and buildspec detection
2. **CloudFront not updating**: Wait 5-15 minutes for invalidation
3. **S3 sync failures**: Check AWS credentials and bucket permissions
4. **Branch detection fails**: Verify CodeBuild environment variables

### Verification Steps
1. Check deployment logs for environment confirmation
2. Verify S3 bucket contents match expected files
3. Test CloudFront URL after invalidation completes
4. Confirm DNS resolution for custom domains

## Next Steps
1. Configure DNS for `dev.dataiesb.com`
2. Set up SSL certificates for custom domains
3. Implement monitoring and alerting
4. Add automated testing in deployment pipeline
