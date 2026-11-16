```
The Nautilus DevOps team is strategizing the migration of a portion of their infrastructure to the AWS cloud. Recognizing the scale of this undertaking, they have opted to approach the migration in incremental steps rather than as a single massive transition. To achieve this, they have segmented large tasks into smaller, more manageable units. This granular approach enables the team to execute the migration in gradual phases, ensuring smoother implementation and minimizing disruption to ongoing operations. By breaking down the migration into smaller tasks, the Nautilus DevOps team can systematically progress through each stage, allowing for better control, risk mitigation, and optimization of resources throughout the migration process.

For this task, create an AMI from an existing EC2 instance named datacenter-ec2 using Terraform.

Name of the AMI should be datacenter-ec2-ami, make sure AMI is in available state.

The Terraform working directory is /home/bob/terraform. Update the main.tf file (do not create a separate .tf file) to create the AMI.

Note: Right-click under the EXPLORER section in VS Code and select Open in Integrated Terminal to launch the terminal.


sol:

aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=datacenter-ec2" \
  --query "Reservations[].Instances[].[InstanceId,State.Name]" \
  --output table

  

# Provision EC2 instance
resource "aws_instance" "ec2" {
  ami           = "ami-0c101f26f147fa7fd"
  instance_type = "t2.micro"
  vpc_security_group_ids = [
    "sg-92175a13a71859a13"
  ]

  tags = {
    Name = "datacenter-ec2"
  }
}

resource "aws_ami_from_instance" "datacenter_ami" {
  name               = "datacenter-ec2-ami"
  source_instance_id = "i-4de37020074bb9093"
}
