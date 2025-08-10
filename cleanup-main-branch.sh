#!/bin/bash

echo "🧹 Main Branch Cleanup Script"
echo "============================="
echo ""

# Check current status
echo "📋 Current branch status:"
git branch -a
echo ""

echo "🎯 Steps to complete main branch cleanup:"
echo ""

echo "1. 🌐 Update GitHub Default Branch (REQUIRED FIRST):"
echo "   - Go to: https://github.com/Data-iesb/Data-IESB/settings"
echo "   - Under 'Default branch', change from 'main' to 'dev'"
echo "   - Click 'Update' and confirm"
echo "   - This MUST be done before deleting the remote main branch"
echo ""

echo "2. 🔄 After changing GitHub default branch, run these commands:"
echo ""
echo "   # Update remote HEAD to point to dev"
echo "   git remote set-head origin dev"
echo ""
echo "   # Delete remote main branch (ONLY after step 1 is complete)"
echo "   git push origin --delete main"
echo ""

echo "3. ✅ Verification commands:"
echo "   git branch -a"
echo "   git remote show origin"
echo ""

echo "⚠️  IMPORTANT WARNINGS:"
echo "   - You MUST change the GitHub default branch FIRST"
echo "   - Do NOT delete the remote main branch until GitHub default is changed"
echo "   - Make sure all team members are aware of the branch change"
echo ""

echo "🎯 Current Status:"
if git branch -r | grep -q "origin/main"; then
    echo "   ❌ Remote main branch still exists"
    echo "   ❌ Need to update GitHub default branch first"
else
    echo "   ✅ Remote main branch has been deleted"
fi

if git remote show origin | grep -q "HEAD branch: dev"; then
    echo "   ✅ Remote HEAD points to dev"
else
    echo "   ❌ Remote HEAD still points to main"
fi

echo ""
echo "📞 Need help? Check BRANCH-MIGRATION-COMPLETE.md for detailed instructions"
