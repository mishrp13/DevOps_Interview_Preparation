
variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "project" {
  description = "Project name"
  type        = string
  default     = "three-tier-app"
}

variable "env" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "state_bucket_name" {
  description = "Globally unique S3 state bucket name"
  type        = string
}
