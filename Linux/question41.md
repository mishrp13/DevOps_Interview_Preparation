```
How do you check which user ran a command or logged in? (last, history, auditd)

“To investigate user activity in Linux, I use different tools depending on what I need to verify. I use last to check login history, history to inspect commands saved in a user's shell history, and auditd with ausearch to investigate command executions when auditing rules are configured. I also correlate timestamps with system and application logs using journalctl. For security investigations, I prefer audit logs over shell history because shell history can be modified or incomplete. I also verify that auditing was enabled and that the relevant logs are available.”

Memorize: last = logins, history = saved shell commands, auditd = configured security auditing.


5. Practical DevOps troubleshooting sequence
Suppose someone restarted Nginx unexpectedly.
1

Check login history
last -n 20

2

Check available shell history
sudo cat /home/ubuntu/.bash_history

3
Search audit records
sudo ausearch -m EXECVE -ts today -i

4

Correlate with service logs
sudo journalctl -u nginx --since today