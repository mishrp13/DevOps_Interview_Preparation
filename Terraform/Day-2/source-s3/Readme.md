```

We will create a secure AWS S3 bucket using Terraform with all the requested security features.
What we are building


Resource	                                             Purpose
aws_s3_bucket	                                        Creates the S3 bucket
aws_s3_bucket_versioning	                            Enables object versioning
aws_s3_bucket_server_side_encryption_configuration	    Enables SSE-KMS encryption
aws_s3_bucket_public_access_block	                    Blocks public access using all 4 flags
aws_s3_bucket_lifecycle_configuration	                Transitions objects to Standard-IA and removes old versions
aws_s3_bucket_policy	                                 Denies requests that do not use HTTPS
aws_kms_key	                                             Creates a customer-managed KMS encryption key
aws_s3_bucket_ownership_controls	                    Disables ACL-based ownership management



Important details:
- SSE-KMS uses a customer-managed KMS key with automatic rotation enabled.
- The lifecycle rule applies to all objects in the bucket.
- Noncurrent versions expire 90 days after becoming noncurrent, not 90 days after their original upload.
- Standard-IA has a 30-day minimum storage duration, and lifecycle transitions can incur charges. Small objects may also be excluded from transitions by S3's default minimum object-size behavior.
- The bucket policy explicitly denies non-TLS requests, including requests otherwise authorized by IAM.
- The KMS key requires appropriate KMS permissions for applications that upload or read encrypted objects. This configuration does not grant application access automatically.