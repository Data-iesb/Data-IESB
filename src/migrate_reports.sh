#!/bin/bash

# Migration script using AWS CLI to move reports from old location to new bucket
# From: s3://dataiesb/reports/ 
# To: s3://dataiesb-reports/

set -e

OLD_BUCKET="dataiesb"
OLD_PREFIX="reports/"
NEW_BUCKET="dataiesb-reports"

echo "🚀 DataIESB Reports Migration (AWS CLI)"
echo "========================================"
echo "📂 Source: s3://$OLD_BUCKET/$OLD_PREFIX"
echo "📂 Target: s3://$NEW_BUCKET/"
echo "========================================"

# Check if buckets exist
echo "🔍 Verifying bucket access..."
if ! aws s3 ls "s3://$OLD_BUCKET" >/dev/null 2>&1; then
    echo "❌ Cannot access s3://$OLD_BUCKET"
    exit 1
fi

if ! aws s3 ls "s3://$NEW_BUCKET" >/dev/null 2>&1; then
    echo "❌ Cannot access s3://$NEW_BUCKET"
    exit 1
fi

echo "✅ Both buckets accessible"

# List existing reports
echo ""
echo "🔍 Scanning for existing reports..."
REPORTS=$(aws s3 ls "s3://$OLD_BUCKET/$OLD_PREFIX" --recursive | grep "\.py$" | awk '{print $4}')

if [ -z "$REPORTS" ]; then
    echo "✅ No Python reports found in old location. Migration not needed."
    exit 0
fi

echo "📋 Found reports to migrate:"
echo "$REPORTS" | while read -r report; do
    echo "  📄 $report"
done

REPORT_COUNT=$(echo "$REPORTS" | wc -l)
echo "📊 Total reports to migrate: $REPORT_COUNT"

# Ask for confirmation
echo ""
read -p "🤔 Proceed with migration? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Migration cancelled."
    exit 0
fi

# Perform migration
echo ""
echo "🔄 Starting migration..."

SUCCESS_COUNT=0
FAIL_COUNT=0

echo "$REPORTS" | while read -r old_key; do
    if [ -n "$old_key" ]; then
        # Extract report ID: reports/5/main.py -> 5
        REPORT_ID=$(echo "$old_key" | cut -d'/' -f2)
        FILENAME=$(echo "$old_key" | cut -d'/' -f3)
        NEW_KEY="$REPORT_ID/$FILENAME"
        
        echo "📦 Migrating report $REPORT_ID..."
        echo "  📂 From: s3://$OLD_BUCKET/$old_key"
        echo "  📂 To: s3://$NEW_BUCKET/$NEW_KEY"
        
        # Copy file
        if aws s3 cp "s3://$OLD_BUCKET/$old_key" "s3://$NEW_BUCKET/$NEW_KEY"; then
            echo "  ✅ Successfully migrated report $REPORT_ID"
            ((SUCCESS_COUNT++))
        else
            echo "  ❌ Failed to migrate report $REPORT_ID"
            ((FAIL_COUNT++))
        fi
        echo ""
    fi
done

echo "========================================"
echo "📊 Migration Summary:"
echo "  ✅ Successful: $SUCCESS_COUNT"
echo "  ❌ Failed: $FAIL_COUNT"
echo "========================================"

if [ $SUCCESS_COUNT -gt 0 ]; then
    echo ""
    echo "🗑️ Clean up old files?"
    echo "The old files are still in s3://$OLD_BUCKET/$OLD_PREFIX"
    read -p "Delete old files after successful migration? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "🧹 Cleaning up old files..."
        
        echo "$REPORTS" | while read -r old_key; do
            if [ -n "$old_key" ]; then
                REPORT_ID=$(echo "$old_key" | cut -d'/' -f2)
                echo "🗑️ Deleting s3://$OLD_BUCKET/$old_key"
                
                if aws s3 rm "s3://$OLD_BUCKET/$old_key"; then
                    echo "  ✅ Deleted report $REPORT_ID from old location"
                else
                    echo "  ⚠️ Failed to delete report $REPORT_ID from old location"
                fi
            fi
        done
        
        echo "✅ Cleanup completed!"
    else
        echo "ℹ️ Old files preserved. You can delete them manually later."
    fi
fi

echo ""
echo "🎉 Migration process completed!"
echo ""
echo "📋 Next steps:"
echo "1. Verify reports are accessible in the admin interface"
echo "2. Test upload functionality with new Lambda function"
echo "3. Deploy the updated Lambda function if not already done"

echo ""
echo "🔍 Current bucket contents:"
echo "📂 New bucket (s3://$NEW_BUCKET):"
aws s3 ls "s3://$NEW_BUCKET/" --recursive

echo ""
echo "📂 Old location (s3://$OLD_BUCKET/$OLD_PREFIX):"
aws s3 ls "s3://$OLD_BUCKET/$OLD_PREFIX" --recursive || echo "  (empty or no access)"
