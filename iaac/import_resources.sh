#!/bin/bash

# Import existing DynamoDB tables
terraform import aws_dynamodb_table.team_members DataIESB-TeamMembers
terraform import aws_dynamodb_table.reports dataiesb-reports

# Import existing S3 buckets
terraform import aws_s3_bucket.website dataiesb
terraform import aws_s3_bucket.reports dataiesb-reports

# Import existing Cognito resources (you'll need the actual IDs)
# terraform import aws_cognito_user_pool.dataiesb <user-pool-id>
# terraform import aws_cognito_user_pool_client.dataiesb <client-id>

# Import existing Route53 zone (you'll need the zone ID)
# terraform import aws_route53_zone.dataiesb <zone-id>

# Import existing ACM certificate (you'll need the certificate ARN)
# terraform import aws_acm_certificate.dataiesb <certificate-arn>

echo "Import the commented resources above with their actual IDs"
