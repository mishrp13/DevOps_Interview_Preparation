```
•os vs pathlib vs shutil?

Python os vs pathlib vs shutil — DevOps Interview Preparation
In DevOps, all three modules are used for file handling, directory management, automation scripts, log management, backups, and deployment tasks.
The main difference is:
- os → Interact with the operating system.
- pathlib → Work with file and directory paths in a clean, modern way.
- shutil → Perform high-level file operations like copying, moving, deleting, and archiving.

os module — Operating system interaction
Interview answer: The os module provides an interface to interact with the operating system. In DevOps, it is commonly used to access environment variables, manage directories, inspect processes, and automate system-level tasks.
Example 1: Access environment variables

import os

env = os.getenv("ENVIRONMENT", "dev")
print(env)

DevOps use case: Identify whether a deployment is running in dev, staging, or production.
Example 2: Create and list directories

import os

os.makedirs("/tmp/app/logs", exist_ok=True)

print(os.listdir("/tmp/app"))

exist_ok=True prevents an error when the directory already exists.

Example 3: Get process ID

import os

print(os.getpid())

DevOps use case: Logging, process monitoring, and troubleshooting automation scripts.



********************************************************************************

pathlib module — Modern path handling
Interview answer: pathlib provides an object-oriented approach to managing file and directory paths. It makes code more readable and portable across Linux, Windows, and macOS.
Example 1: Check if a file exists

from pathlib import Path

file = Path("/var/log/app.log")

if file.exists():
    print("Log file exists")
else:
    print("Log file missing")

DevOps use case: Check whether a configuration or log file exists before running an automation task.

Example 2: Find all .log files

from pathlib import Path

log_dir = Path("/var/log")

for file in log_dir.glob("*.log"):
    print(file)

 glob("*.log") searches the given directory. Use rglob("*.log") to search recursively.

 Example 3: Build paths

 from pathlib import Path

base = Path("/opt/app")
config = base / "config" / "settings.yaml"

print(config)

Output:

/opt/app/config/settings.yaml

The / operator joins path components.

This is generally cleaner than:

import os

config = os.path.join(
    "/opt/app", "config", "settings.yaml"
)

shutil module — File operations and backups
Interview answer: shutil is used for high-level file operations such as copying, moving, deleting directory trees, and creating archives. It is useful for DevOps backup and deployment automation.
Example 1: Copy configuration file

import shutil

shutil.copy2(
    "/opt/app/config.yaml",
    "/tmp/config.yaml"
)

copy2() copies file contents and attempts to preserve metadata, such as modification timestamps.
DevOps use case: Backup configuration before deployment.
Example 2: Move log files

import shutil

shutil.move(
    "/tmp/app.log",
    "/backup/app.log"
)

DevOps use case: Log rotation and archiving.

Example 3: Remove a directory

import shutil

shutil.rmtree("/tmp/old_build")

DevOps use case: Clean old build artifacts after CI/CD execution.
Be careful: rmtree() recursively deletes the directory and its contents.
Example 4: Check disk usage

import shutil

total, used, free = shutil.disk_usage("/")

print(f"Free space: {free / (1024**3):.2f} GB")

DevOps use case: Check disk space before deploying an application.

5. Real DevOps scenario — Use all three together
Interview question: Write a Python script to check whether an application log exists, create a backup directory, and copy the log into it.


import os
from pathlib import Path
import shutil

# Get environment
env = os.getenv("ENVIRONMENT", "dev")

# Define paths
log_file = Path("/var/log/app.log")
backup_dir = Path("/tmp/backups")

# Create backup directory
backup_dir.mkdir(parents=True, exist_ok=True)

# Check and copy
if log_file.is_file():
    shutil.copy2(
        log_file,
        backup_dir / f"{env}_app.log"
    )
    print("Backup completed")
else:
    print("Log file not found")


    Module                                               Responsibility
    os                                            Read deployment environment
    pathlib                                       Manage paths and check file existence
    shutil                                        Copy log file into backup directory




In Python DevOps automation, I use os for interacting with the operating system, especially environment variables and process information. I use pathlib for clean, cross-platform file path management, checking file existence, and locating configuration files. I use shutil for high-level file operations like copying build artifacts, moving logs, creating backups, and cleaning directories. These three modules are often used together in CI/CD pipelines and deployment automation.

Easy way to remember:
- os = Operating System
- pathlib = Where is the file?
- shutil = What should I do with the file?
For a DevOps interview, prioritize os.getenv(), Path.exists(), Path.glob(), shutil.copy2(), shutil.copytree(), shutil.rmtree(), and shutil.disk_usage().
