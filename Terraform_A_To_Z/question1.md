```
The Nautilus DevOps team is strategizing the migration of a portion of their infrastructure to the AWS cloud. Recognizing the scale of this undertaking, they have opted to approach the migration in incremental steps rather than as a single massive transition. To achieve this, they have segmented large tasks into smaller, more manageable units. This granular approach enables the team to execute the migration in gradual phases, ensuring smoother implementation and minimizing disruption to ongoing operations. By breaking down the migration into smaller tasks, the Nautilus DevOps team can systematically progress through each stage, allowing for better control, risk mitigation, and optimization of resources throughout the migration process.

For this task, create a key pair using Terraform with the following requirements:

Name of the key pair should be xfusion-kp.

Key pair type must be rsa.

The private key file should be saved under /home/bob/devops-kp.pem.


sol:


terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
    tls = {
      source  = "hashicorp/tls"
    }
    local = {
      source  = "hashicorp/local"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "tls_private_key" "xfusion_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "xfusion_kp" {
  key_name   = "xfusion-kp"
  key_type   = "rsa"
  public_key = tls_private_key.xfusion_key.public_key_openssh
}

resource "local_sensitive_file" "private_key" {
  content         = tls_private_key.xfusion_key.private_key_pem
  filename        = "/home/bob/xfusion-kp.pem"
  file_permission = "0400"
}


