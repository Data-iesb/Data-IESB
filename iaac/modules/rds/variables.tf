# Variables
variable "env_prefix" {
  description = "Environment name (e.g., prod, dev, staging)"
  type        = string
  default     = "prod"
}


variable "vpc_id" {
  description = "VPC ID"
  type        = string
}



variable "public_subnets" {
  description = "List of public subnets for RDS"
  type        = list(string)
}

variable "secret_name" {
  description = "The name of the secret in AWS Secrets Manager"
  type        = string
  default     = "rds-secret"
}

variable "rds_instance_class" {
  description = "Instance type for the RDS instance"
  type        = string
  default     = "db.t3.medium"
}

# Outputs

output "rds_host" {
  description = "RDS endpoint (hostname)"
  value       = aws_db_instance.rds.endpoint
}

output "rds_secret_arn" {
  description = "Secrets Manager ARN storing DB credentials"
  value       = data.aws_secretsmanager_secret.rds_secret
}
