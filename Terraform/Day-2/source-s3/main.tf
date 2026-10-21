
# 1. Create S3 bucket
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name

  # Prevent accidental deletion of nonempty bucket
  force_destroy = false

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# 2. Enable versioning
resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id

  versioning_configuration {
    status = "Enabled"
  }
}

# 3. Create customer-managed KMS key
resource "aws_kms_key" "s3" {
  description             = "KMS key for S3 encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}

resource "aws_kms_alias" "s3" {
  name          = "alias/${var.bucket_name}-s3"
  target_key_id = aws_kms_key.s3.key_id
}

# 4. Enable SSE-KMS encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }

    bucket_key_enabled = true
  }
}

# 5. Block all public access
resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.this.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 6. Disable ACLs
resource "aws_s3_bucket_ownership_controls" "this" {
  bucket = aws_s3_bucket.this.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# 7. Configure lifecycle rules
resource "aws_s3_bucket_lifecycle_configuration" "this" {
  bucket = aws_s3_bucket.this.id

  depends_on = [
    aws_s3_bucket_versioning.this
  ]

  rule {
    id     = "transition-and-cleanup"
    status = "Enabled"

    filter {}

    # Transition current objects after 30 days
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    # Delete noncurrent versions after 90 days
    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

# 8. Deny requests without HTTPS
data "aws_iam_policy_document" "deny_insecure" {
  statement {
    sid    = "DenyInsecureTransport"
    effect = "Deny"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = ["s3:*"]

    resources = [
      aws_s3_bucket.this.arn,
      "${aws_s3_bucket.this.arn}/*"
    ]

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "this" {
  bucket = aws_s3_bucket.this.id
  policy = data.aws_iam_policy_document.deny_insecure.json

  depends_on = [
    aws_s3_bucket_public_access_block.this
  ]
}





# Important details:
# - SSE-KMS uses a customer-managed KMS key with automatic rotation enabled.
# - The lifecycle rule applies to all objects in the bucket.
# - Noncurrent versions expire 90 days after becoming noncurrent, not 90 days after their original upload.
# - Standard-IA has a 30-day minimum storage duration, and lifecycle transitions can incur charges. Small objects may also be excluded from transitions by S3's default minimum object-size behavior.
# - The bucket policy explicitly denies non-TLS requests, including requests otherwise authorized by IAM.
# - The KMS key requires appropriate KMS permissions for applications that upload or read encrypted objects. This configuration does not grant application access automatically.