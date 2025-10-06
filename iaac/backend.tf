terraform {
  backend "s3" {
    bucket         = "iesb-terraform"
    key            = "state/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}
