```
Q.  Disk is 100% full. How do you find what is using it? (Also: disk is full but df shows space, which points to inodes or deleted-but-open files)


If a Linux disk is 100% full, I first run `df -h` to identify the affected filesystem. Then I use `du -xhd1` to find the directories consuming the most space and `find` to identify large files.

If disk usage reported by `df` does not match what I can see with `du`, I check `df -i` for inode exhaustion and `lsof +L1` for deleted files that are still open by running processes.

After identifying the root cause, I safely clean up unnecessary files, investigate log rotation or application behavior, and verify the recovery using `df -h`. In production, I avoid deleting files or restarting services without understanding the impact.

Remember this interview sequence: df -h → du → find → df -i → lsof +L1.




