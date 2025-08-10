#!/bin/bash

# GitHub Repository Settings Update Script
# This script changes the default branch from main to dev and updates branch protection

echo "🔧 Updating GitHub repository settings..."

# Repository details
REPO_OWNER="Data-iesb"
REPO_NAME="Data-IESB"

echo "📋 Repository: $REPO_OWNER/$REPO_NAME"
echo ""

# Note: This requires GitHub CLI (gh) to be installed and authenticated
# Or you can manually update these settings in GitHub web interface

echo "🔄 Manual steps required in GitHub web interface:"
echo ""
echo "1. Go to: https://github.com/$REPO_OWNER/$REPO_NAME/settings"
echo "2. In 'General' settings, under 'Default branch':"
echo "   - Change from 'main' to 'dev'"
echo "   - Click 'Update'"
echo ""
echo "3. In 'Branches' settings:"
echo "   - Update branch protection rules for 'prod' (formerly main)"
echo "   - Set up branch protection for 'dev' as the new default"
echo ""
echo "4. Update CodeBuild project to use 'prod' branch for production builds"
echo ""
echo "5. Update any webhooks or integrations to use correct branches"
echo ""

# Create branch mapping documentation
cat > ../BRANCH-MAPPING.md << 'EOF'
# Branch Mapping - Data IESB

## Branch Structure Update

### 🔄 Branch Renaming
- **main** → **prod** (Production branch)
- **dev** → **dev** (Development branch, now default)

### 🎯 Branch Purposes

#### 🚀 prod (Production)
- **Purpose**: Production deployments
- **Environment**: Production
- **Region**: sa-east-1 (São Paulo)
- **S3 Bucket**: dataiesb
- **CloudFront**: E371T2F886B5KI
- **Domain**: https://dataiesb.com
- **Deployment**: AWS CodeBuild with buildspec.yml

#### 🧪 dev (Development - Default)
- **Purpose**: Development and testing
- **Environment**: Development
- **Region**: us-east-1 (N. Virginia)
- **S3 Bucket**: dev-dataiesb
- **CloudFront**: E142Z1CPAKR8S8
- **URL**: https://d2v66tm8wx23ar.cloudfront.net
- **Target**: https://dev.dataiesb.com
- **Deployment**: GitHub Actions

### 🔧 Required Updates

#### GitHub Settings
- [x] Create prod branch from main
- [ ] Change default branch from main to dev
- [ ] Update branch protection rules
- [ ] Delete old main branch (after verification)

#### AWS CodeBuild
- [ ] Update project to build from 'prod' branch instead of 'main'
- [ ] Update buildspec.yml branch detection logic

#### Documentation
- [ ] Update all references from main to prod
- [ ] Update deployment documentation
- [ ] Update README files

### 🚦 Workflow
1. **Development**: Work on feature branches, merge to `dev`
2. **Testing**: Test changes in development environment
3. **Production**: Create PR from `dev` to `prod` for production releases

### 🔗 URLs
- **Development**: https://d2v66tm8wx23ar.cloudfront.net
- **Production**: https://dataiesb.com
EOF

echo "✅ Branch mapping documentation created: BRANCH-MAPPING.md"
echo ""
echo "🎯 Next steps:"
echo "1. Manually update GitHub settings as described above"
echo "2. Update AWS CodeBuild project settings"
echo "3. Test both environments"
echo "4. Delete old main branch after verification"
