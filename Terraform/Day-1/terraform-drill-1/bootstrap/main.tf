
# 1. Create S3 bucket

resource "aws_s3_bucket" "terraform_state" {
  bucket = var.state_bucket_name

  lifecycle {
    prevent_destroy = true
  }
}

# 2. Enable bucket versioning

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

# 3. Enable server-side encryption

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# 4. Block all public access

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 5. Enforce TLS for S3 requests

data "aws_iam_policy_document" "require_tls" {
  statement {
    sid    = "DenyInsecureTransport"
    effect = "Deny"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = ["s3:*"]

    resources = [
      aws_s3_bucket.terraform_state.arn,
      "${aws_s3_bucket.terraform_state.arn}/*"
    ]

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "require_tls" {
  bucket = aws_s3_bucket.terraform_state.id
  policy = data.aws_iam_policy_document.require_tls.json

  depends_on = [
    aws_s3_bucket_public_access_block.terraform_state
  ]
}



# Why each resource matters
# Resource	                                                 Purpose
# aws_s3_bucket	                                        Stores Terraform state
# aws_s3_bucket_versioning	                     Keeps previous state versions for recovery
# aws_s3_bucket_server_side_encryption_configuration	Explicitly configures encryption at rest
# aws_s3_bucket_public_access_block	                     Prevents public access
# aws_s3_bucket_policy	                                       Denies requests made without TLS
# prevent_destroy	                                  Protects the bucket from accidental Terraform destruction

# S3 versioning is particularly important. If the state is accidentally overwritten, 
#an administrator can recover an earlier version. HashiCorp also recommends enabling 
#versioning for S3 state buckets