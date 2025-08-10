# Data IESB Development Environment

This document describes the development infrastructure and deployment process for the Data IESB website.

## 🏗️ Infrastructure Overview

### AWS Resources Created

#### S3 Bucket
- **Name**: `dev-dataiesb`
- **Region**: `us-east-1`
- **Purpose**: Static website hosting for development
- **Website Endpoint**: http://dev-dataiesb.s3-website-us-east-1.amazonaws.com

#### CloudFront Distribution
- **Distribution ID**: `E142Z1CPAKR8S8`
- **Domain**: https://d2v66tm8wx23ar.cloudfront.net
- **Target Custom Domain**: dev.dataiesb.com
- **Status**: InProgress (deployment in progress)

#### DynamoDB Table
- **Name**: `DataIESB-TeamMembers`
- **Shared**: Yes (same table used for production)
- **Purpose**: Dynamic team member data

## 🚀 Deployment Process

### Automatic Deployment (Recommended)
1. Push changes to the `dev` branch
2. GitHub Actions automatically deploys to development environment
3. CloudFront cache is invalidated automatically
4. Changes are live within 5-15 minutes

### Manual Deployment
```bash
# Ensure you're on dev branch
git checkout dev

# Run deployment script
./deploy-dev.sh
```

## 🌐 Access URLs

### Current Access Points
- **CloudFront (Temporary)**: https://d2v66tm8wx23ar.cloudfront.net
- **S3 Direct**: http://dev-dataiesb.s3-website-us-east-1.amazonaws.com

### Target Domain
- **Custom Domain**: https://dev.dataiesb.com (requires DNS configuration)

## 📋 Development Workflow

### Branch Structure
- `main` → Production environment
- `dev` → Development environment

### Making Changes
1. Create feature branch from `dev`
2. Make your changes
3. Test locally
4. Create PR to `dev` branch
5. After merge, changes auto-deploy to development

## 🔧 Configuration Files

- `deploy-dev.sh` - Manual deployment script
- `.github/workflows/deploy-dev.yml` - GitHub Actions workflow
- `dev-config.json` - Environment configuration
- `DEV-README.md` - This documentation

## 🎯 Features Enabled

- ✅ Dynamic team data loading from DynamoDB
- ✅ Professional color templates (miv.html)
- ✅ Consistent brand styling
- ✅ Responsive design
- ✅ Role-based team member display
- ✅ Automated deployments

## 🔄 Next Steps

### DNS Configuration
1. Add CNAME record: `dev.dataiesb.com` → `d2v66tm8wx23ar.cloudfront.net`
2. Or use Route 53 for better integration

### SSL Certificate
1. Request certificate in AWS Certificate Manager
2. Validate domain ownership
3. Update CloudFront distribution

### Monitoring
1. Set up CloudWatch alarms
2. Configure access logging
3. Monitor deployment success/failures

## 🛠️ Troubleshooting

### Common Issues

**Deployment fails**
- Check AWS credentials in GitHub Secrets
- Verify S3 bucket permissions
- Check CloudFront distribution status

**Changes not visible**
- Wait 5-15 minutes for CloudFront cache
- Check if invalidation was created
- Verify files were uploaded to S3

**Team data not loading**
- Check DynamoDB table access
- Verify team-data.js is deployed
- Check browser console for errors

## 📞 Support

For issues with the development environment:
1. Check GitHub Actions logs
2. Review AWS CloudWatch logs
3. Contact the DevOps team (Roberto)

---

**Environment**: Development  
**Last Updated**: 2025-08-10  
**Maintained by**: Roberto Moreira Diniz
