#!/usr/bin/env python3
"""
Migration script to move existing reports from s3://dataiesb/reports/ to s3://dataiesb-reports/
This script will:
1. List all reports in the old location (s3://dataiesb/reports/)
2. Copy them to the new bucket (s3://dataiesb-reports/)
3. Verify the copy was successful
4. Optionally delete from old location after confirmation
"""

import boto3
import sys
from botocore.exceptions import ClientError

def migrate_reports():
    """Migrate reports from old bucket structure to new bucket"""
    
    # Initialize S3 client
    s3_client = boto3.client('s3')
    
    # Bucket configurations
    OLD_BUCKET = 'dataiesb'
    OLD_PREFIX = 'reports/'
    NEW_BUCKET = 'dataiesb-reports'
    
    print("🚀 Starting DataIESB Reports Migration...")
    print("=" * 60)
    print(f"📂 Source: s3://{OLD_BUCKET}/{OLD_PREFIX}")
    print(f"📂 Target: s3://{NEW_BUCKET}/")
    print("=" * 60)
    
    try:
        # List all objects in the old location
        print("🔍 Scanning for existing reports...")
        
        response = s3_client.list_objects_v2(
            Bucket=OLD_BUCKET,
            Prefix=OLD_PREFIX
        )
        
        if 'Contents' not in response:
            print("✅ No reports found in old location. Migration not needed.")
            return
        
        reports_to_migrate = []
        for obj in response['Contents']:
            key = obj['Key']
            if key.endswith('.py'):  # Only migrate Python files
                # Extract report ID from path: reports/5/main.py -> 5
                parts = key.split('/')
                if len(parts) >= 3:
                    report_id = parts[1]  # reports/5/main.py -> 5
                    filename = parts[2]   # reports/5/main.py -> main.py
                    
                    reports_to_migrate.append({
                        'old_key': key,
                        'new_key': f"{report_id}/{filename}",
                        'report_id': report_id,
                        'size': obj['Size']
                    })
        
        if not reports_to_migrate:
            print("✅ No Python report files found to migrate.")
            return
        
        print(f"📋 Found {len(reports_to_migrate)} reports to migrate:")
        total_size = 0
        for report in reports_to_migrate:
            print(f"  📄 Report {report['report_id']}: {report['old_key']} -> {report['new_key']} ({report['size']} bytes)")
            total_size += report['size']
        
        print(f"📊 Total size to migrate: {total_size} bytes")
        print()
        
        # Ask for confirmation
        response = input("🤔 Proceed with migration? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Migration cancelled by user.")
            return
        
        # Perform migration
        print("\n🔄 Starting migration...")
        successful_migrations = []
        failed_migrations = []
        
        for i, report in enumerate(reports_to_migrate, 1):
            print(f"📦 [{i}/{len(reports_to_migrate)}] Migrating report {report['report_id']}...")
            
            try:
                # Copy object to new bucket
                copy_source = {
                    'Bucket': OLD_BUCKET,
                    'Key': report['old_key']
                }
                
                s3_client.copy_object(
                    CopySource=copy_source,
                    Bucket=NEW_BUCKET,
                    Key=report['new_key'],
                    MetadataDirective='COPY'
                )
                
                # Verify the copy was successful
                try:
                    s3_client.head_object(Bucket=NEW_BUCKET, Key=report['new_key'])
                    successful_migrations.append(report)
                    print(f"  ✅ Successfully migrated to s3://{NEW_BUCKET}/{report['new_key']}")
                except ClientError:
                    failed_migrations.append(report)
                    print(f"  ❌ Failed to verify migration for report {report['report_id']}")
                
            except ClientError as e:
                failed_migrations.append(report)
                print(f"  ❌ Failed to migrate report {report['report_id']}: {e}")
        
        # Migration summary
        print("\n" + "=" * 60)
        print("📊 Migration Summary:")
        print(f"  ✅ Successful: {len(successful_migrations)}")
        print(f"  ❌ Failed: {len(failed_migrations)}")
        
        if failed_migrations:
            print("\n❌ Failed migrations:")
            for report in failed_migrations:
                print(f"  - Report {report['report_id']}: {report['old_key']}")
        
        if successful_migrations:
            print(f"\n✅ Successfully migrated {len(successful_migrations)} reports!")
            print("\n🗑️ Clean up old files?")
            print("The old files are still in s3://dataiesb/reports/")
            cleanup_response = input("Delete old files after successful migration? (y/N): ").strip().lower()
            
            if cleanup_response == 'y':
                print("\n🧹 Cleaning up old files...")
                for report in successful_migrations:
                    try:
                        s3_client.delete_object(Bucket=OLD_BUCKET, Key=report['old_key'])
                        print(f"  🗑️ Deleted s3://{OLD_BUCKET}/{report['old_key']}")
                    except ClientError as e:
                        print(f"  ⚠️ Failed to delete s3://{OLD_BUCKET}/{report['old_key']}: {e}")
                
                print("✅ Cleanup completed!")
            else:
                print("ℹ️ Old files preserved. You can delete them manually later.")
        
        print("\n🎉 Migration process completed!")
        print("\n📋 Next steps:")
        print("1. Verify reports are accessible in the admin interface")
        print("2. Test upload functionality with new Lambda function")
        print("3. Update any hardcoded references to old bucket structure")
        
    except ClientError as e:
        print(f"❌ AWS Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def verify_buckets():
    """Verify that both buckets exist and are accessible"""
    s3_client = boto3.client('s3')
    
    print("🔍 Verifying bucket access...")
    
    buckets_to_check = ['dataiesb', 'dataiesb-reports']
    
    for bucket in buckets_to_check:
        try:
            s3_client.head_bucket(Bucket=bucket)
            print(f"  ✅ s3://{bucket} - accessible")
        except ClientError as e:
            print(f"  ❌ s3://{bucket} - error: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🏗️ DataIESB Reports Migration Tool")
    print("This tool will migrate reports from the old bucket structure to the new one.")
    print()
    
    # Verify bucket access first
    if not verify_buckets():
        print("❌ Cannot access required buckets. Please check your AWS credentials and permissions.")
        sys.exit(1)
    
    # Run migration
    migrate_reports()
