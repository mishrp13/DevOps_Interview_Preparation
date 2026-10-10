```
What does exit code 137 mean? (OOM killed or SIGKILL)


Exit code 137 in Docker generally means that the container's main process was terminated by signal 9, which is SIGKILL.

The number 137 comes from 128 + 9, where 9 represents SIGKILL.

A common reason is an Out-Of-Memory (OOM) event, where the container exceeds its memory limit and the Linux kernel kills the process. However, exit code 137 does not always mean an OOM kill; the process could also have been forcefully terminated using SIGKILL.

To troubleshoot this issue, I check the container status using `docker ps -a`, inspect the container using `docker inspect`, check whether `OOMKilled` is true, review the application logs, and investigate memory usage and limits.

Based on the findings, I may optimize the application, investigate memory leaks, adjust the container memory limit, or increase available host memory.  