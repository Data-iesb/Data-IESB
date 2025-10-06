data "aws_secretsmanager_secret" "rds_secret" {
  name = "rds-secret"
}

data "aws_secretsmanager_secret_version" "rds_secret_value" {
  secret_id = data.aws_secretsmanager_secret.rds_secret.id
}

# Fetch subnet IDs dynamically for public subnets
data "aws_subnets" "public_subnets" {
  filter {
    name   = "cidr-block"
    values = var.public_subnets
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "rds-security-group"
  description = "Allow PostgreSQL access"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Public access, restrict in production
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-sg-${var.env_prefix}"
  }
}

resource "aws_db_instance" "rds" {
  identifier             = "rds-${var.env_prefix}"
  engine                = "postgres"
  engine_version        = "17"
  instance_class        = "db.t3.medium"
  allocated_storage     = 20
  publicly_accessible   = true
  db_name              = jsondecode(data.aws_secretsmanager_secret_version.rds_secret_value.secret_string)["db_name"]
  username            = jsondecode(data.aws_secretsmanager_secret_version.rds_secret_value.secret_string)["username"]
  password            = jsondecode(data.aws_secretsmanager_secret_version.rds_secret_value.secret_string)["password"]
  skip_final_snapshot  = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.rds_public_subnet_group.name  # ✅ Use new subnet group

  tags = {
    Name        = "rds-${var.env_prefix}"
    Environment = var.env_prefix
  }
}


# Create RDS Subnet Group using dynamically retrieved public subnet IDs
resource "aws_db_subnet_group" "rds_public_subnet_group" {
  name        = "${var.env_prefix}-rds-public-subnet-group"
  description = "RDS subnet group for public access"
  subnet_ids  = data.aws_subnets.public_subnets.ids

  tags = {
    Name        = "${var.env_prefix}-rds-public-subnet-group"
    Environment = var.env_prefix
  }
}


