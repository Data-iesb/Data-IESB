#!/bin/bash

# Script to check current state of both buckets

echo "🔍 DataIESB Bucket Analysis"
echo "=========================="

echo ""
echo "📂 OLD LOCATION: s3://dataiesb/reports/"
echo "----------------------------------------"
aws s3 ls s3://dataiesb/reports/ --recursive | grep "\.py$" || echo "  (no Python files found)"

echo ""
echo "📂 NEW LOCATION: s3://dataiesb-reports/"
echo "----------------------------------------"
aws s3 ls s3://dataiesb-reports/ --recursive | grep "\.py$" || echo "  (no Python files found)"

echo ""
echo "📊 SUMMARY:"
OLD_COUNT=$(aws s3 ls s3://dataiesb/reports/ --recursive | grep "\.py$" | wc -l)
NEW_COUNT=$(aws s3 ls s3://dataiesb-reports/ --recursive | grep "\.py$" | wc -l)

echo "  📄 Reports in old location: $OLD_COUNT"
echo "  📄 Reports in new location: $NEW_COUNT"

if [ $OLD_COUNT -gt 0 ] && [ $NEW_COUNT -eq 0 ]; then
    echo ""
    echo "⚠️  MIGRATION NEEDED!"
    echo "   Reports are still in the old location and need to be migrated."
    echo "   Run: bash migrate_reports.sh"
elif [ $OLD_COUNT -gt 0 ] && [ $NEW_COUNT -gt 0 ]; then
    echo ""
    echo "🔄 PARTIAL MIGRATION"
    echo "   Reports exist in both locations. Check if migration is complete."
elif [ $OLD_COUNT -eq 0 ] && [ $NEW_COUNT -gt 0 ]; then
    echo ""
    echo "✅ MIGRATION COMPLETE"
    echo "   All reports are in the new location."
else
    echo ""
    echo "❓ NO REPORTS FOUND"
    echo "   No reports found in either location."
fi
