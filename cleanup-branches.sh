#!/bin/bash

echo "🧹 Cleaning up branch structure..."
echo "⚠️  Make sure you've changed the default branch to 'dev' on GitHub first!"
echo ""

# Confirm before proceeding
read -p "Have you changed the default branch to 'dev' on GitHub? (y/N): " confirm
if [[ $confirm != [yY] ]]; then
    echo "❌ Please change the default branch on GitHub first:"
    echo "   1. Go to https://github.com/Data-iesb/Data-IESB/settings/branches"
    echo "   2. Change default branch from 'main' to 'dev'"
    echo "   3. Then run this script again"
    exit 1
fi

echo "🗑️  Deleting remote main branch..."
git push origin --delete main

echo "🔄 Updating remote HEAD reference..."
git remote set-head origin dev

echo "🧹 Cleaning up remote tracking references..."
git remote prune origin

echo "✅ Branch cleanup complete!"
echo ""
echo "📋 Current branch structure:"
git branch -a

echo ""
echo "🎯 Recommended workflow:"
echo "  • dev (default) - Development environment"
echo "  • prod - Production environment"
