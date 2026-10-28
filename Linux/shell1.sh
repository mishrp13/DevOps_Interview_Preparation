#!/bin/bash

LOG_DIR="/var/log/myapp"
LOG_FILE="/var/log/myapp/log_rotation.log"

# Check if log directory exists
if [ ! -d "$LOG_DIR" ]; then
    echo "[$(date)] ERROR: Log directory does not exist" >&2
    exit 1
fi

# Compress .log files older than 7 days
find "$LOG_DIR" -type f -name "*.log" ! -name "log_rotation.log" -mtime +7 \
    -exec gzip {} \; \
    -exec sh -c 'echo "[$(date)] Compressed: $1" >> "$2"' _ {} "$LOG_FILE" \;

# Delete compressed .gz files older than 30 days
find "$LOG_DIR" -type f -name "*.gz" -mtime +30 \
    -exec sh -c '
        file="$1"
        log="$2"
        if rm -f "$file"; then
            echo "[$(date)] Deleted: $file" >> "$log"
        fi
    ' _ {} "$LOG_FILE" \;

echo "[$(date)] Log rotation completed" >> "$LOG_FILE"