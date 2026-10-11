```
Q . A server is slow. How do you investigate? (CPU, memory, disk I/O, network, in that order)



If a server is slow, I investigate systematically in the order of CPU, memory, disk I/O, and network.

First, I use `top`, `uptime`, and `mpstat` to check CPU utilization, load average, and resource-heavy processes.

Second, I use `free -h`, `vmstat`, and process memory usage to check available RAM, swapping, and possible memory leaks.

Third, I use `iostat -xz`, `df -h`, and `df -i` to investigate disk latency, I/O bottlenecks, disk space, and inode exhaustion.

Fourth, I check network errors and connections using `ip -s link` and `ss`, and test connectivity and response times using `ping` and `curl`.

Finally, I correlate the results with system logs, application logs, monitoring metrics, and recent deployments. I identify the root cause before applying a fix, then verify that performance has recovered.