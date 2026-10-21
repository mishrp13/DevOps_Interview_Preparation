
terraform {
  backend "s3" {
    bucket       = "your-unique-tf-state-12345"
    key          = "dev/network/terraform.tfstate"
    region       = "ap-south-1"
    encrypt      = true
    use_lockfile = true
  }
}


