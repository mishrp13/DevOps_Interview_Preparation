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