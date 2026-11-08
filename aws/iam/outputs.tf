output "app_role_arn" {
  description = "ARN of the app compute role"
  value       = aws_iam_role.app.arn
}
