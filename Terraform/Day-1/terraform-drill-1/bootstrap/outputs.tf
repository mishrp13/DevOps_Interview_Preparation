
output "state_bucket_name" {
  description = "Terraform remote state bucket"
  value       = aws_s3_bucket.terraform_state.id
}

output "state_bucket_arn" {
  description = "Terraform remote state bucket ARN"
  value       = aws_s3_bucket.terraform_state.arn
}
