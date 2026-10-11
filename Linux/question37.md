```
You cannot SSH into a server. What do you check?


If I cannot SSH into a server, I troubleshoot step by step.

First, I verify the server IP and network connectivity. Then I check whether TCP port 22 is reachable using `nc` and run `ssh -vvv` to identify where the connection fails.

If the port is unreachable, I investigate routing, firewalls, cloud security groups, and network ACLs. If the connection is refused, I check whether the SSH daemon is running and listening on the correct port.

If I reach the authentication stage, I verify the username, SSH key, key permissions, and server-side SSH configuration. Finally, I check server health, system logs, and cloud VM status checks.

Once I identify and fix the root cause, I retry SSH and verify that access works securely.

Remember this interview sequence: Network → Port → SSH service → Firewall/security rules → Authentication → Server health.