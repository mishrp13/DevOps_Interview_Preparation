```
As part of the data migration process, the Nautilus DevOps team is actively creating several S3 buckets on AWS. They plan to utilize both private and public S3 buckets to store the relevant data. Given the ongoing migration of other infrastructure to AWS, it is logical to consolidate data storage within the AWS environment as well.

Create a public S3 bucket named xfusion-s3-190723871 using Terraform.

Ensure the bucket is accessible publicly once created by setting the proper ACL.

The Terraform working directory is /home/bob/terraform. Create the main.tf file (do not create a different .tf file) to accomplish this task.

Notes:

Create the resources only in the us-east-1 region.
Right-click under the EXPLORER section in VS Code and select Open in Integrated Terminal to launch the terminal.
The name of the S3 bucket should be based on xfusion-s3-190723871.
You can use the ACL settings to ensure the bucket is publicly accessible.

-------------------------------------------


provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "xfusion_bucket" {
  bucket = "xfusion-s3-190723871"
}

resource "aws_s3_bucket_ownership_controls" "ownership" {
  bucket = aws_s3_bucket.xfusion_bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket = aws_s3_bucket.xfusion_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.xfusion_bucket.id
  acl    = "public-read"

  depends_on = [
    aws_s3_bucket_ownership_controls.ownership,
    aws_s3_bucket_public_access_block.public_access
  ]
}
