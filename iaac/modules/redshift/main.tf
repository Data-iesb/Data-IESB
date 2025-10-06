
resource "aws_network_acl" "redshift_acl" {
  vpc_id = var.vpc_id
  subnet_ids = var.public_subnet_ids

  # Allow inbound Redshift traffic (TCP 5439) from anywhere (Adjust CIDR as needed)
  ingress {
    rule_no    = 100
    action     = "allow"
    protocol   = "tcp"
    from_port  = 5439
    to_port    = 5439
    cidr_block = "0.0.0.0/0"
  }

  # Allow all outbound traffic
  egress {
    rule_no    = 100
    action     = "allow"
    protocol   = "-1"
    from_port  = 0
    to_port    = 0
    cidr_block = "0.0.0.0/0"
  }

  tags = {
    Name = "${var.env_prefix}-redshift-acl"
  }
}

resource "aws_network_acl_association" "redshift_acl_association" {
  count = length(var.public_subnet_ids)

  network_acl_id = aws_network_acl.redshift_acl.id
  subnet_id      = var.public_subnet_ids[count.index]
}

resource "aws_security_group" "redshift_sg" {
  vpc_id = var.vpc_id
  name   = "${var.env_prefix}-redshift-sg"

  # ✅ Allow inbound connections on Redshift's port 5439 from anywhere
  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # 🌍 Public access (adjust for security)
  }

  # ✅ Ensure Redshift can send responses to any external client
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # Allow all outbound traffic
  }

  tags = {
    Name = "${var.env_prefix}-redshift-sg"
  }
}


data "aws_secretsmanager_secret_version" "redshift_secret" {
  secret_id = "redshift-secret"
}

locals {
  redshift_creds = jsondecode(data.aws_secretsmanager_secret_version.redshift_secret.secret_string)
}

resource "aws_redshift_cluster" "redshift" {
  cluster_identifier        = "${var.env_prefix}-redshift"
  database_name             = local.redshift_creds["db_name"]
  master_username           = local.redshift_creds["username"]
  master_password           = local.redshift_creds["password"]
  node_type           = "dc2.large"
  cluster_type        = "single-node"

  publicly_accessible       = true
  skip_final_snapshot       = true
  vpc_security_group_ids    = [aws_security_group.redshift_sg.id]
  cluster_subnet_group_name = aws_redshift_subnet_group.redshift_subnet_group.name

  tags = {
    Name = "${var.env_prefix}-redshift"
  }
}


resource "aws_redshift_subnet_group" "redshift_subnet_group" {
  name       = "${var.env_prefix}-redshift-subnet-group"
  subnet_ids = var.public_subnet_ids  # ✅ Use public subnet IDs from root module

  tags = {
    Name = "${var.env_prefix}-redshift-subnet-group"
  }
}
 
