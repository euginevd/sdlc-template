output "bucket_name" {
  description = "Name of the app data bucket"
  value       = aws_s3_bucket.data.bucket
}
