```
How do you safely patch a fleet of servers?

“To safely patch a fleet of servers, I first check server health, available updates, backups, and the maintenance window. I patch a test server first, validate the application, and then use automation tools like Ansible or a patch management platform to roll out updates in controlled batches. I use a canary deployment and rolling patching strategy to avoid taking all servers down simultaneously. Before patching each server, I drain it from the load balancer if necessary. After patching, I reboot if required and verify services, application health checks, logs, and monitoring metrics. If any batch fails, I stop the rollout and follow the rollback or recovery plan. Finally, I document the patch versions and confirm compliance.”

Remember this sequence: Assess → Backup → Test → Canary → Roll out gradually → Verify → Recover if needed → Document.