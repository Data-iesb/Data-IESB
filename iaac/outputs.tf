output "website_bucket_name" {
  description = "Name of the S3 bucket for website"
  value       = aws_s3_bucket.website.id
}

output "reports_bucket_name" {
  description = "Name of the S3 bucket for reports"
  value       = aws_s3_bucket.reports.id
}

output "website_endpoint" {
  description = "Website endpoint"
  value       = aws_s3_bucket_website_configuration.website.website_endpoint
}

output "cognito_user_pool_id" {
  description = "Cognito User Pool ID"
  value       = aws_cognito_user_pool.dataiesb.id
}

output "cognito_client_id" {
  description = "Cognito User Pool Client ID"
  value       = aws_cognito_user_pool_client.dataiesb.id
}

output "route53_zone_id" {
  description = "Route 53 Hosted Zone ID"
  value       = aws_route53_zone.dataiesb.zone_id
}

output "certificate_arn" {
  description = "ACM Certificate ARN"
  value       = aws_acm_certificate.dataiesb.arn
}

output "dynamodb_team_members_table" {
  description = "DynamoDB Team Members table name"
  value       = aws_dynamodb_table.team_members.name
}

output "dynamodb_reports_table" {
  description = "DynamoDB Reports table name"
  value       = aws_dynamodb_table.reports.name
}

output "codebuild_website_project" {
  description = "CodeBuild project for website"
  value       = aws_codebuild_project.data_iesb_prod.name
}

output "codebuild_report_project" {
  description = "CodeBuild project for report app"
  value       = aws_codebuild_project.dataiesb_report.name
}
