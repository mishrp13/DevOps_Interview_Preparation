```
A process is using high CPU. How do you find and fix it?

If a process is consuming high CPU, I first use `top` or `ps` to identify the process ID and CPU utilization.

Next, I inspect the process details, parent process, and thread-level CPU usage. I check application logs, monitoring metrics, traffic patterns, and recent deployments to find the root cause.

Based on the findings, I might optimize the application, reduce excessive workload, scale the service, or restart it if necessary and safe. I avoid killing a process blindly, especially in production.

Finally, I verify CPU usage, system load, application health, and logs to confirm that the issue is resolved.

Remember: Finding a high-CPU process is only the first step. In a DevOps interview, explain how you identify the root cause, minimize service disruption, and verify the fix.


uptime
top
ps -eo pid,comm,%cpu --sort=-%cpu | head
ps -fp <PID>
top -H -p <PID>
sudo journalctl -u <service-name> -n 100 --no-pager
sudo systemctl restart <service-name>
systemctl status <service-name>



Step-by-step commands
1

Check overall CPU and load
uptime
top


Say: “First, I check the system load and identify whether CPU usage is high.”



2

Find the top CPU-consuming processes
ps -eo pid,ppid,comm,%cpu,%mem --sort=-%cpu | head


Say: “I sort processes by CPU usage to identify the process ID.”



3

Inspect the process
ps -fp <PID>


Replace <PID> with the actual process ID.
Say: “I check the process owner, start time, and command to understand what is running.”



4

Check thread-level CPU usage
top -H -p <PID>


Say: “If it is a multithreaded application, I check whether a particular thread is consuming excessive CPU.”



5

Check application or service logs
sudo journalctl -u <service-name> -n 100 --no-pager


Say: “I check logs and recent deployments to identify the root cause.”



6

Fix the issue
If a service restart is justified and safe:
sudo systemctl restart <service-name>


Say: “After identifying the cause, I apply the appropriate fix. I avoid killing processes blindly in production.”



7

Verify recovery
top
uptime
systemctl status <service-name>


Say: “Finally, I confirm CPU usage has reduced and the service is healthy.”