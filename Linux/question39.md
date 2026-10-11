```
Out of memory: what is the OOM killer, and how do you know it killed something? (dmesg)

The OOM Killer is a Linux kernel mechanism that terminates processes when the system faces severe memory pressure and needs to reclaim memory. To check whether a process was killed, I first run free -h to check memory usage. Then I check sudo dmesg -T | grep -i -E 'oom|killed process|out of memory' for kernel messages. If needed, I check journalctl -k for historical kernel logs. After identifying the affected process, I investigate memory consumption, application logs, and service health. Finally, I fix the root cause, such as a memory leak, excessive workload, or an insufficient memory limit, and monitor the system.”

Remember the interview flow: Memory usage → Kernel logs (dmesg) → Identify killed process → Find root cause → Fix and monitor.