```
Q. A service will not start. Where do you look?

If a service does not start, I first check its status using `systemctl status`. Then I inspect the service logs using `journalctl -u service-name` to identify the exact error.

Next, I validate the configuration, check whether the required port is already in use, verify dependencies and file permissions, and check system resources such as memory and disk space.

After identifying and fixing the root cause, I restart the service and verify its status and application health. I avoid repeatedly restarting the service without understanding the failure, especially in production.

Remember this order: Status → Logs → Configuration → Ports → Dependencies → Permissions → Resources → Restart and verify.