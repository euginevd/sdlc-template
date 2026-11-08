data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
  partition  = data.aws_partition.current.partition
  # Every role Terraform creates carries the bootstrap stack's permissions boundary.
  boundary_arn = "arn:${local.partition}:iam::${local.account_id}:policy/${var.project}-boundary"
}

# Role for the app's compute (Lambda or ECS tasks) to read and write the app's data buckets.
resource "aws_iam_role" "app" {
  name                 = "${var.project}-app-${var.environment}"
  description          = "App compute role for ${var.project} ${var.environment}"
  permissions_boundary = local.boundary_arn

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = ["lambda.amazonaws.com", "ecs-tasks.amazonaws.com"] }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "app_data" {
  name = "app-data"
  role = aws_iam_role.app.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = "arn:${local.partition}:s3:::${var.project}-app-*"
      },
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject"]
        Resource = "arn:${local.partition}:s3:::${var.project}-app-*/*"
      },
    ]
  })
}
