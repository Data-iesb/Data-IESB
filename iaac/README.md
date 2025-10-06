# DataIESB Infrastructure as Code

This directory contains Terraform configurations for the DataIESB platform infrastructure.

## Architecture

The infrastructure includes:

- **DynamoDB Tables**: `DataIESB-TeamMembers` and `dataiesb-reports`
- **S3 Buckets**: `dataiesb` (website) and `dataiesb-reports` (data storage)
- **Cognito**: User authentication and authorization
- **Route 53**: DNS management for `dataiesb.com`
- **ACM**: SSL/TLS certificates
- **Lambda**: API backend functions
- **API Gateway**: REST API endpoints

## Files

- `main.tf` - Core infrastructure resources
- `lambda.tf` - Lambda functions and API Gateway
- `variables.tf` - Input variables
- `outputs.tf` - Output values
- `terraform.tfvars.example` - Example variables file

## Usage

### Prerequisites

1. AWS CLI configured with appropriate credentials
2. Terraform >= 1.0 installed

### Import Existing Resources

Since the resources already exist, you'll need to import them:

```bash
# Initialize Terraform
terraform init

# Import existing resources
terraform import aws_dynamodb_table.team_members DataIESB-TeamMembers
terraform import aws_dynamodb_table.reports dataiesb-reports
terraform import aws_s3_bucket.website dataiesb
terraform import aws_s3_bucket.reports dataiesb-reports

# Import other resources as needed
# terraform import aws_cognito_user_pool.dataiesb <user-pool-id>
# terraform import aws_route53_zone.dataiesb <zone-id>
# terraform import aws_acm_certificate.dataiesb <certificate-arn>
```

### Plan and Apply

```bash
# Create terraform.tfvars from example
cp terraform.tfvars.example terraform.tfvars

# Review planned changes
terraform plan

# Apply changes (if any)
terraform apply
```

## Notes

- Lambda function deployment is handled by the CI/CD pipeline
- The `lambda_placeholder.zip` file is ignored in lifecycle management
- Certificate validation requires manual DNS record verification if not using Route 53
