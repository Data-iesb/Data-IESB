variable "env_prefix" {
  default = "prod"
}

variable "subnet_cidr_block" {
  default = "10.0.1.0/24"
}

variable "private_subnets" {
  description = "The private subnets for RDS instances"
  type        = list(string)
}


variable "public_subnets" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}


variable "vpc_cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "enable_nat_gateway" {
  description = "Whether to enable a NAT gateway"
  type        = bool
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs"
  type        = list(string)
}

