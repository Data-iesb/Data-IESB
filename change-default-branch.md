# Change Default Branch to Dev

## Why Change to Dev Branch as Default?

✅ **Protect Production**: Prevents accidental changes to the live site  
✅ **Safe for Beginners**: New contributors work in development environment first  
✅ **Better Workflow**: All changes tested in dev before going to production  
✅ **Reduced Risk**: Main branch stays stable and production-ready  

## Steps to Change Default Branch on GitHub

### Method 1: GitHub Web Interface (Recommended)

1. **Go to Repository Settings**
   - Navigate to: https://github.com/Data-iesb/Data-IESB
   - Click on **Settings** tab
   - Click on **General** in the left sidebar

2. **Change Default Branch**
   - Scroll down to **Default branch** section
   - Click the switch icon next to "main"
   - Select **dev** from the dropdown
   - Click **Update**
   - Confirm the change by clicking **I understand, update the default branch**

3. **Verify Change**
   - The default branch should now show as `dev`
   - New clones will automatically checkout `dev` branch

### Method 2: GitHub CLI (If you have gh CLI installed)

```bash
# Change default branch using GitHub CLI
gh repo edit Data-iesb/Data-IESB --default-branch dev
```

## Update Local Repository

After changing the default branch on GitHub, update your local repository:

```bash
# Fetch latest changes
git fetch origin

# Set dev as the default branch locally
git remote set-head origin dev

# Switch to dev branch if not already there
git checkout dev

# Verify the change
git remote show origin | grep "HEAD branch"
```

## Update Documentation

Update any documentation that references the main branch:

1. **README.md** - Update branch references
2. **Contributing guidelines** - Update workflow instructions
3. **Issue templates** - Update default branch references

## Branch Protection Rules (Recommended)

After changing the default branch, set up protection rules:

### For `dev` branch:
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Include administrators

### For `main` branch:
- ✅ Require pull request reviews (2+ reviewers)
- ✅ Require status checks to pass
- ✅ Restrict pushes to specific people/teams
- ✅ Include administrators

## Workflow After Change

### New Contributors:
1. Clone repository → automatically gets `dev` branch
2. Create feature branch from `dev`
3. Submit PR to `dev` branch
4. Changes tested in development environment
5. After approval, changes can be promoted to `main`

### Deployment Flow:
```
feature-branch → dev → (testing) → main → production
```

## Benefits

- 🛡️ **Production Protection**: Main branch stays stable
- 🧪 **Testing Environment**: All changes tested in dev first
- 👥 **Team Safety**: New team members can't accidentally break production
- 🔄 **Better CI/CD**: Clear separation between dev and prod deployments
- 📊 **Quality Control**: Review process before production deployment

## Commands Summary

```bash
# After GitHub default branch change:
git fetch origin
git remote set-head origin dev
git checkout dev

# Verify:
git remote show origin | grep "HEAD branch"
# Should show: HEAD branch: dev
```

---

**Next Steps:**
1. Change default branch on GitHub (Method 1 above)
2. Update local repository
3. Set up branch protection rules
4. Update team documentation
5. Notify team members of the change
