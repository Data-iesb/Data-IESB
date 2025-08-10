# GitHub Setup Checklist for Dev-First Workflow

## ✅ Completed (Automatically)
- [x] Created `dev` branch with complete infrastructure
- [x] Set up GitHub Actions for auto-deployment
- [x] Created comprehensive documentation
- [x] Added issue and PR templates
- [x] Set up CODEOWNERS file
- [x] Deployed development environment

## 🔧 Manual Steps Required on GitHub

### 1. Change Default Branch (CRITICAL)
**Priority: HIGH** - Do this first to protect production!

1. Go to: https://github.com/Data-iesb/Data-IESB/settings
2. Click **General** in left sidebar
3. Scroll to **Default branch** section
4. Click switch icon next to "main"
5. Select **dev** from dropdown
6. Click **Update**
7. Confirm: **"I understand, update the default branch"**

**Result**: New clones will get `dev` branch (safe for beginners)

### 2. Set Up Branch Protection Rules
**Priority: HIGH** - Protect both branches

#### For `dev` branch:
1. Go to: https://github.com/Data-iesb/Data-IESB/settings/branches
2. Click **Add rule**
3. Branch name pattern: `dev`
4. Enable:
   - [x] Require a pull request before merging
   - [x] Require approvals: **1**
   - [x] Dismiss stale PR approvals when new commits are pushed
   - [x] Require status checks to pass before merging
   - [x] Require branches to be up to date before merging
   - [x] Require conversation resolution before merging
5. Click **Create**

#### For `main` branch:
1. Click **Add rule** again
2. Branch name pattern: `main`
3. Enable:
   - [x] Require a pull request before merging
   - [x] Require approvals: **2**
   - [x] Dismiss stale PR approvals when new commits are pushed
   - [x] Require review from CODEOWNERS
   - [x] Require status checks to pass before merging
   - [x] Require branches to be up to date before merging
   - [x] Restrict pushes that create files that match a pattern
   - [x] Require conversation resolution before merging
   - [x] Include administrators
4. Click **Create**

### 3. Configure GitHub Secrets (If not already set)
**Priority: MEDIUM** - For automated deployments

1. Go to: https://github.com/Data-iesb/Data-IESB/settings/secrets/actions
2. Add these secrets:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

### 4. Set Up Team Permissions (Optional)
**Priority: LOW** - For better collaboration

1. Go to: https://github.com/Data-iesb/Data-IESB/settings/access
2. Create teams:
   - **data-iesb-admins**: Roberto, Leonardo
   - **data-iesb-developers**: All team members
   - **data-iesb-contributors**: External contributors
3. Assign appropriate permissions

### 5. Enable Discussions (Optional)
**Priority: LOW** - For team communication

1. Go to: https://github.com/Data-iesb/Data-IESB/settings
2. Scroll to **Features**
3. Check **Discussions**

## 🎯 Verification Steps

After completing the manual steps:

### 1. Test Default Branch
```bash
# Clone fresh repository
git clone https://github.com/Data-iesb/Data-IESB.git test-clone
cd test-clone
git branch
# Should show: * dev (not main)
```

### 2. Test Branch Protection
- Try to push directly to `dev` → Should be blocked
- Try to push directly to `main` → Should be blocked
- Create PR to `dev` → Should require 1 approval
- Create PR to `main` → Should require 2 approvals

### 3. Test Auto-Deployment
```bash
# Make a small change on dev branch
echo "<!-- Test change -->" >> src/index.html
git add .
git commit -m "test: verify auto-deployment"
git push origin dev
```
- Check GitHub Actions tab
- Verify deployment to: https://d2v66tm8wx23ar.cloudfront.net

## 📋 Team Communication

### Notify Team Members
Send this message to the team:

---
**🚨 Important: Repository Workflow Change**

We've updated our development workflow for better collaboration and production safety:

**New Default Branch**: `dev` (was `main`)
- New contributors automatically get the safe development branch
- All new features should be developed on `dev` first
- Production (`main`) is now protected

**For Existing Contributors**:
```bash
git fetch origin
git checkout dev
git pull origin dev
```

**New Workflow**:
1. Create feature branch from `dev`
2. Submit PR to `dev` (auto-deploys to development)
3. After testing, promote to `main` (production)

**Development URL**: https://d2v66tm8wx23ar.cloudfront.net
**Production URL**: https://dataiesb.com

Questions? Check the updated README.md or ask Roberto.

---

## 🔄 Rollback Plan (If Needed)

If something goes wrong, you can quickly rollback:

1. Change default branch back to `main`
2. Remove branch protection rules
3. Revert the last commit on `dev`

## 📞 Support

If you need help with any of these steps:
- Check the documentation in the repository
- Contact Roberto (DevOps lead)
- Create an issue using the new templates

---

**Status**: ⏳ Waiting for manual GitHub configuration  
**Priority**: 🔥 HIGH - Change default branch ASAP  
**Estimated Time**: 15-20 minutes for all steps
