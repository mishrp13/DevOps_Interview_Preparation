```
.An application cannot reach a database. Walk through your debugging steps?.

“First, I check the application status and logs to identify the exact database connection error. Then I verify the database hostname using getent hosts and test the database port using nc -zv. If the port is unreachable, I investigate routing, firewall rules, cloud security groups, and database listening configuration. If the port is reachable, I check the database service, credentials, user permissions, connection limits, and database logs. After fixing the root cause, I test connectivity again, verify application health, and monitor the logs to confirm the issue is resolved.”

Commands to memorize:
sudo systemctl status myapp
sudo journalctl -u myapp -n 100 --no-pager
getent hosts <DB_HOST>
nc -zv <DB_HOST> 3306
sudo systemctl status mysql
sudo ss -ltnp | grep ':3306'


Interview tip: If asked which issue you would check first, say you would start with the exact application error rather than randomly restarting the application or database. The error guides the next diagnostic step.