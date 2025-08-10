# Deployment Configuration - Data IESB

## Overview
The Data IESB project uses separate deployment configurations for production and development environments with a new branch structure.

## Branch Structure (Updated)

### 🚀 prod Branch (Production)
- **Environment**: Production
- **Region**: `sa-east-1` (São Paulo)
- **S3 Bucket**: `dataiesb`
- **CloudFront Distribution**: `E371T2F886B5KI`
- **Domain**: `https://dataiesb.com`
- **Deployment Method**: AWS CodeBuild with `buildspec.yml`
- **Status**: ✅ Working

### 🧪 dev Branch (Development - Default)
- **Environment**: Development
- **Region**: `us-east-1` (N. Virginia)
- **S3 Bucket**: `dev-dataiesb`
- **CloudFront Distribution**: `E142Z1CPAKR8S8`
- **Temporary URL**: `https://d2v66tm8wx23ar.cloudfront.net`
- **Target Domain**: `https://dev.dataiesb.com` (pending DNS setup)
- **Deployment Method**: GitHub Actions (`.github/workflows/deploy-dev.yml`)
- **Status**: ✅ Working

## Buildspec Files

### 1. `buildspec.yml` (Production - prod Branch)
- **Purpose**: Production deployment for prod branch
- **Configuration**: Hardcoded production values
- **Features**:
  - Simple, reliable YAML structure
  - Direct S3 sync to production bucket
  - CloudFront invalidation for production
  - Clear production-focused logging

### 2. `buildspec-dev-simple.yml` (Development)
- **Purpose**: Development deployment configuration
- **Use Case**: Manual development builds if needed
- **Configuration**: Hardcoded development values

## Deployment Process

### Production Deployment (prod Branch)
1. Create PR from `dev` to `prod` branch
2. Merge PR after review and approval
3. AWS CodeBuild triggers automatically
4. Uses `buildspec.yml` with production settings
5. Deploys to production S3 bucket (`dataiesb`)
6. Invalidates production CloudFront (`E371T2F886B5KI`)
7. Site available at `https://dataiesb.com`

### Development Deployment (dev Branch)
1. Push to `dev` branch (default branch)
2. GitHub Actions triggers automatically (`.github/workflows/deploy-dev.yml`)
3. Deploys to development S3 bucket (`dev-dataiesb`)
4. Invalidates development CloudFront (`E142Z1CPAKR8S8`)
5. Site available at `https://d2v66tm8wx23ar.cloudfront.net`

## Environment Variables

### Production (prod Branch)
```bash
ENVIRONMENT=production
REGION=sa-east-1
S3_BUCKET=dataiesb
CLOUDFRONT_DISTRIBUTION_ID=E371T2F886B5KI
SITE_URL=https://dataiesb.com
```

### Development (dev Branch)
```bash
ENVIRONMENT=development
REGION=us-east-1
S3_BUCKET=dev-dataiesb
CLOUDFRONT_DISTRIBUTION_ID=E142Z1CPAKR8S8
SITE_URL=https://d2v66tm8wx23ar.cloudfront.net
```

## Branch Migration

### ✅ Completed Steps
- [x] Created `prod` branch from `main`
- [x] Synced `dev` branch with latest changes
- [x] Updated buildspec.yml for prod branch
- [x] Updated deployment documentation
- [x] Created branch mapping documentation

### 🔄 Pending Steps
- [ ] Change GitHub default branch from `main` to `dev`
- [ ] Update AWS CodeBuild to use `prod` branch
- [ ] Update branch protection rules
- [ ] Test both environments
- [ ] Delete old `main` branch

## Security & Best Practices

### Branch Protection
- prod branch requires pull request reviews
- No direct pushes to prod branch
- Status checks must pass before merging
- dev branch is now the default for new development

### AWS Permissions
- Separate IAM roles for production and development
- Least privilege access principles
- Environment-specific resource access

### Deployment Safety
- Production uses explicit prod branch configuration
- Development uses GitHub Actions for reliability
- Both environments have separate AWS resources

## Workflow

### Development Workflow
1. **Feature Development**: Create feature branch from `dev`
2. **Testing**: Merge feature to `dev` for testing in development environment
3. **Production Release**: Create PR from `dev` to `prod` for production deployment

### Branch Structure
```
dev (default) ← feature branches
 ↓ (PR for production release)
prod (production) → AWS CodeBuild → https://dataiesb.com
```

## Troubleshooting

### Common Issues
1. **Build fails**: Check if CodeBuild is configured for `prod` branch
2. **Wrong environment**: Verify branch-specific configurations
3. **CloudFront not updating**: Wait 5-15 minutes for invalidation
4. **Default branch**: Ensure GitHub default is set to `dev`

### Verification Steps
1. Check that `dev` is the default branch in GitHub
2. Verify CodeBuild project uses `prod` branch
3. Test development deployment from `dev` branch
4. Test production deployment from `prod` branch

## Next Steps
1. Complete GitHub repository settings update
2. Update AWS CodeBuild project configuration
3. Test both deployment pipelines
4. Configure DNS for `dev.dataiesb.com`
5. Set up monitoring and alerting

## Build Status
- **Production (prod)**: ✅ Ready with updated buildspec.yml
- **Development (dev)**: ✅ Working with GitHub Actions
- **Branch Migration**: 🔄 In Progress
- **Last Updated**: 2025-08-10
