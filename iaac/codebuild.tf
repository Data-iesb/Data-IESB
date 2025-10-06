# IAM Role for CodeBuild
resource "aws_iam_role" "codebuild_role" {
  name = "codebuild-data-iesb-service-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "codebuild.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "CodeBuild DataIESB Role"
    Environment = var.environment
    Project     = var.project_name
  }
}

# IAM Policy for CodeBuild
resource "aws_iam_role_policy" "codebuild_policy" {
  name = "codebuild-data-iesb-policy"
  role = aws_iam_role.codebuild_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.website.arn,
          "${aws_s3_bucket.website.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "cloudfront:CreateInvalidation"
        ]
        Resource = "*"
      }
    ]
  })
}

# CodeBuild Project for DataIESB Website
resource "aws_codebuild_project" "data_iesb_prod" {
  name         = "data-iesb-prod-build"
  description  = "CodeBuild project for Data IESB production environment"
  service_role = aws_iam_role.codebuild_role.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/amazonlinux-x86_64-standard:5.0"
    type         = "LINUX_CONTAINER"
  }

  source {
    type            = "GITHUB"
    location        = "https://github.com/Data-iesb/Data-IESB.git"
    git_clone_depth = 1
    buildspec       = "buildspec.yml"
  }

  tags = {
    Project     = "DataIESB"
    Environment = "Production"
  }
}

# GitHub Webhook for DataIESB
resource "aws_codebuild_webhook" "data_iesb_prod" {
  project_name = aws_codebuild_project.data_iesb_prod.name
  build_type   = "BUILD"

  filter_group {
    filter {
      type    = "EVENT"
      pattern = "PUSH"
    }
    filter {
      type    = "HEAD_REF"
      pattern = "^refs/heads/prod$"
    }
  }
}

# IAM Role for Report App CodeBuild
resource "aws_iam_role" "codebuild_report_role" {
  name = "codebuild-dataiesb-relatorios"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "codebuild.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "CodeBuild Report App Role"
    Environment = var.environment
    Project     = var.project_name
  }
}

# IAM Policy for Report App CodeBuild
resource "aws_iam_role_policy" "codebuild_report_policy" {
  name = "codebuild-report-policy"
  role = aws_iam_role.codebuild_report_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:GetAuthorizationToken",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "eks:DescribeCluster",
          "eks:UpdateKubeconfig"
        ]
        Resource = "*"
      }
    ]
  })
}

# CodeBuild Project for Report App
resource "aws_codebuild_project" "dataiesb_report" {
  name         = "dataiesb-report"
  service_role = aws_iam_role.codebuild_report_role.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type = "BUILD_GENERAL1_LARGE"
    image        = "aws/codebuild/amazonlinux-x86_64-standard:5.0"
    type         = "LINUX_CONTAINER"

    environment_variable {
      name  = "REPOSITORY_URI"
      value = "248189947068.dkr.ecr.us-east-1.amazonaws.com/dataiesb-site"
    }
  }

  source {
    type            = "GITHUB"
    location        = "https://github.com/Data-iesb/report-app"
    git_clone_depth = 1
    buildspec       = "buildspec.yml"
  }

  tags = {
    Project     = "DataIESB"
    Environment = "Production"
  }
}

# GitHub Webhook for Report App
resource "aws_codebuild_webhook" "dataiesb_report" {
  project_name = aws_codebuild_project.dataiesb_report.name
  build_type   = "BUILD"

  filter_group {
    filter {
      type    = "EVENT"
      pattern = "PUSH"
    }
  }
}
