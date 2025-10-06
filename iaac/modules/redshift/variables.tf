variable "env_prefix" {
  description = "Environment prefix for naming resources"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where Redshift will be deployed"
  type        = string
}

variable "public_subnets" {
  description = "List of public subnet IDs"
  type        = list(string)
}


# List of public subnet IDs
variable "public_subnet_ids" {
  type = list(string)
}

# Map subnet IDs to Availability Zones
variable "subnet_az_map" {
  type = map(string)
}


variable "internet_gateway_id" {
  description = "The ID of the Internet Gateway"
  type        = string
}

