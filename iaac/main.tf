# Use existing VPC and subnets
data "aws_vpc" "existing" {
  id = "vpc-08f71cff199dc1fc6"
}

data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.existing.id]
  }
  filter {
    name   = "tag:Name"
    values = ["Public Subnet*"]
  }
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.existing.id]
  }
  filter {
    name   = "tag:Name"
    values = ["Private Subnet*"]
  }
}

module "rds" {
  source = "./modules/rds"
  env_prefix       = var.env_prefix
  vpc_id           = data.aws_vpc.existing.id
  public_subnets = var.public_subnets
}

# DynamoDB Tables
resource "aws_dynamodb_table" "team_members" {
  name           = "DataIESB-TeamMembers"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "email"

  attribute {
    name = "email"
    type = "S"
  }

  attribute {
    name = "role"
    type = "S"
  }

  global_secondary_index {
    name            = "RoleIndex"
    hash_key        = "role"
    read_capacity   = 5
    write_capacity  = 5
    projection_type = "ALL"
  }

  tags = {
    Name        = "DataIESB-TeamMembers"
    Environment = "production"
    Project     = "DataIESB"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_dynamodb_table" "reports" {
  name           = "dataiesb-reports"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "report_id"

  attribute {
    name = "report_id"
    type = "S"
  }

  attribute {
    name = "user_email"
    type = "S"
  }

  global_secondary_index {
    name            = "user-email-index"
    hash_key        = "user_email"
    projection_type = "ALL"
  }

  tags = {
    Name        = "dataiesb-reports"
    Environment = "production"
    Project     = "DataIESB"
  }

  lifecycle {
    prevent_destroy = true
  }
}

# S3 Buckets
resource "aws_s3_bucket" "website" {
  bucket = "dataiesb"

  tags = {
    Name        = "DataIESB Website"
    Environment = "production"
    Project     = "DataIESB"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket" "reports" {
  bucket = "dataiesb-reports"

  tags = {
    Name        = "DataIESB Reports"
    Environment = "production"
    Project     = "DataIESB"
  }

  lifecycle {
    prevent_destroy = true
  }
}

# S3 Website Configuration
resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }
}

# S3 Public Access Block
resource "aws_s3_bucket_public_access_block" "website" {
  bucket = aws_s3_bucket.website.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# S3 Bucket Policy
resource "aws_s3_bucket_policy" "website" {
  bucket = aws_s3_bucket.website.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.website.arn}/*"
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.website]
}

# Cognito User Pool
resource "aws_cognito_user_pool" "dataiesb" {
  name = "dataiesb-users"

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  auto_verified_attributes = ["email"]

  tags = {
    Name        = "DataIESB User Pool"
    Environment = "production"
    Project     = "DataIESB"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_cognito_user_pool_client" "dataiesb" {
  name         = "dataiesb-client"
  user_pool_id = aws_cognito_user_pool.dataiesb.id

  generate_secret = false
  
  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]

  callback_urls = [
    "https://dataiesb.com/callback.html"
  ]

  logout_urls = [
    "https://dataiesb.com"
  ]

  supported_identity_providers = ["COGNITO"]
}

# Route 53 Hosted Zone
resource "aws_route53_zone" "dataiesb" {
  name = "dataiesb.com"

  tags = {
    Name        = "DataIESB Domain"
    Environment = "production"
    Project     = "DataIESB"
  }

  lifecycle {
    prevent_destroy = true
  }
}

# ACM Certificate
resource "aws_acm_certificate" "dataiesb" {
  domain_name       = "dataiesb.com"
  subject_alternative_names = ["*.dataiesb.com"]
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name        = "DataIESB Certificate"
    Environment = "production"
    Project     = "DataIESB"
  }
}

# Route 53 Certificate Validation - commented out for import
# resource "aws_route53_record" "cert_validation" {
#   for_each = {
#     for dvo in aws_acm_certificate.dataiesb.domain_validation_options : dvo.domain_name => {
#       name   = dvo.resource_record_name
#       record = dvo.resource_record_value
#       type   = dvo.resource_record_type
#     }
#   }

#   allow_overwrite = true
#   name            = each.value.name
#   records         = [each.value.record]
#   ttl             = 60
#   type            = each.value.type
#   zone_id         = aws_route53_zone.dataiesb.zone_id
# }

# resource "aws_acm_certificate_validation" "dataiesb" {
#   certificate_arn         = aws_acm_certificate.dataiesb.arn
#   validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
# }
