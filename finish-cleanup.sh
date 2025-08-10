#!/bin/bash

echo "🏁 Finishing Main Branch Cleanup"
echo "================================"
echo ""

echo "⚠️  Only run this AFTER changing GitHub default branch to 'dev'"
echo ""

read -p "Have you changed the GitHub default branch from 'main' to 'dev'? (y/N): " confirm

if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    echo ""
    echo "🔄 Updating remote HEAD to point to dev..."
    git remote set-head origin dev
    
    echo ""
    echo "🗑️  Deleting remote main branch..."
    git push origin --delete main
    
    echo ""
    echo "✅ Cleanup complete! Verifying..."
    echo ""
    
    echo "📋 Current branches:"
    git branch -a
    
    echo ""
    echo "🔍 Remote info:"
    git remote show origin | grep "HEAD branch"
    
    echo ""
    echo "🎉 Main branch cleanup completed successfully!"
    echo ""
    echo "✅ Summary:"
    echo "   - Local main branch: ❌ Deleted"
    echo "   - Remote main branch: ❌ Deleted"
    echo "   - Default branch: ✅ dev"
    echo "   - Production branch: ✅ prod"
    echo ""
    
else
    echo ""
    echo "❌ Please change the GitHub default branch first:"
    echo "   1. Go to: https://github.com/Data-iesb/Data-IESB/settings"
    echo "   2. Under 'Default branch', change from 'main' to 'dev'"
    echo "   3. Click 'Update' and confirm"
    echo "   4. Then run this script again"
    echo ""
fi
