```

Validate a Terraform or CloudFormation file with a script ?


Difficulty: Beginner to Intermediate
Topics: Python, Terraform, AWS CloudFormation, Infrastructure as Code (IaC), CI/CD

1. Python script (interview-ready)
This script supports both Terraform and CloudFormation using their official validation commands.



import subprocess
import sys
import os


def run_command(command):
    """Execute a command and check its result."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        print("SUCCESS: Validation passed!")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("FAILED: Validation failed!")
        print(e.stderr)
        sys.exit(1)

    except FileNotFoundError:
        print("ERROR: Required CLI tool not installed.")
        sys.exit(1)


def validate_terraform(directory):
    print("Validating Terraform configuration...")

    if not os.path.isdir(directory):
        print("ERROR: Directory does not exist.")
        sys.exit(1)

    run_command([
        "terraform", "-chdir=" + directory,
        "init", "-backend=false", "-input=false"
    ])

    run_command([
        "terraform", "-chdir=" + directory,
        "validate"
    ])


def validate_cloudformation(file_path):
    print("Validating CloudFormation template...")

    if not os.path.isfile(file_path):
        print("ERROR: File does not exist.")
        sys.exit(1)

    run_command([
        "aws", "cloudformation",
        "validate-template",
        "--template-body",
        "file://" + os.path.abspath(file_path)
    ])


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage:")
        print("python validate.py terraform <directory>")
        print("python validate.py cloudformation <file>")
        sys.exit(1)

    tool = sys.argv[1].lower()
    path = sys.argv[2]

    if tool == "terraform":
        validate_terraform(path)

    elif tool == "cloudformation":
        validate_cloudformation(path)

    else:
        print("ERROR: Unsupported tool")
        sys.exit(1)


2. How to execute
Terraform validation

python validate.py terraform ./terraform

Expected output:

Validating Terraform configuration...
SUCCESS: Validation passed!

SUCCESS: Validation passed!
Success! The configuration is valid.


CloudFormation validation

python validate.py cloudformation template.yaml


Expected output (simplified):

Validating CloudFormation template...
SUCCESS: Validation passed!

Prerequisites: Terraform CLI for Terraform validation; AWS CLI with appropriate credentials and permissions for CloudFormation validation.
3. How the script works
Python concept	             Purpose
subprocess.run()	       Executes Terraform or AWS CLI commands
capture_output=True	       Captures command output
check=True	             Raises an exception on command failure
os.path.isdir()	         Checks Terraform directory
os.path.isfile()	     Checks CloudFormation file
try/except	              Handles errors
sys.exit(1)	           Returns a failure code for CI/CD

The script performs validation, not deployment. Terraform validation checks configuration consistency but does not verify all provider-side resources or permissions. CloudFormation validate-template performs template validation but does not guarantee that a stack deployment will succeed.


4. How to explain this in a DevOps interview
Interviewer: How would you validate Terraform or CloudFormation files using Python?

Your answer:
I would use Python's subprocess module to automate Infrastructure as Code validation.

For Terraform, I execute terraform init -backend=false followed by terraform validate to check the configuration.

For AWS CloudFormation, I execute aws cloudformation validate-template using the AWS CLI.

I also implement exception handling to capture validation failures and return a non-zero exit code.

This script can be integrated into a Jenkins or GitHub Actions pipeline to prevent invalid infrastructure configurations from progressing to deployment.