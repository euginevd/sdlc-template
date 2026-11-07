# Copy this folder to aws/<unit>/, then replace <project> and <unit>.
terraform {
  required_version = ">= 1.17"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.72.0"
    }
  }

  # The bucket is passed at init, so the account ID stays out of the repo:
  # terraform init -backend-config="bucket=$TF_STATE_BUCKET"
  backend "s3" {
    key          = "<project>/<unit>.tfstate"
    region       = "ap-southeast-2"
    use_lockfile = true
    encrypt      = true
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Project     = var.project
      Unit        = "<unit>"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
