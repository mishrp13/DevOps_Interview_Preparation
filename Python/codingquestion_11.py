
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
