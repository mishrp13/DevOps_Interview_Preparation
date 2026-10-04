```

1. Explain the Linux directory structure (/etc, /var, /opt, /proc, /tmp)?.

Ans:

/etc (Et cetera)
• Stores system-wide configuration files and shell scripts used to control how programs behave.
• Contains plain text files like /etc/passwd (user accounts) and /etc/fstab (storage mounts).
• Requires root/administrator privileges to edit.

/var (Variable)
• Holds dynamic data that grows or changes frequently while the system runs.
• Stores system logs (/var/log), email spools, print queues, and temporary application cache.
• Prevents static system partitions from filling up with changing data.


/opt (Optional)
• Used for third-party add-on software packages that do not come pre-installed with the core operating system.
• Keeps self-contained applications neatly in their own folders rather than scattering files across /bin or /lib.


/proc (Process)
• Acts as a virtual filesystem generated entirely in the computer's memory by the kernel.
• Contains real-time information about running processes and hardware stats like /proc/cpuinfo.
• Does not take up actual hard drive space; it disappears when the system shuts down


/tmp (Temporary)
• Provides a holding space for temporary files created by applications and users.
• Accessible by any user to read and write data needed during a current session.
• Clears out automatically when the system restarts.