```

A file was deleted but disk space was not freed. Why?

Interview answer to memorize
“In Linux, when a file is deleted, its directory entry is removed. However, if a running process still has the file open, the kernel keeps the file's data on disk until the last open reference is closed. This is common with log files that are deleted before the application closes them. I first check disk usage with df -h, then run sudo lsof +L1 to identify deleted files still held open. I inspect the process, arrange a safe reload or restart if appropriate, and verify disk space again with df -h.”

Remember this command: sudo lsof +L1 — it is the key troubleshooting command for deleted-but-open files.

