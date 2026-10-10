```
The container is running but the app is not reachable. What do you check?


If a Docker container is running but the application is not reachable, I troubleshoot the issue layer by layer.

**Step 1: Check the container status** using `docker ps` to confirm that the container is running.

**Step 2: Check application logs** using `docker logs <container_name>` to identify startup errors, crashes, or configuration issues.

**Step 3: Verify port mapping** using `docker port <container_name>` or `docker ps`. I confirm that the application port inside the container is mapped to the correct host port.

**Step 4: Check whether the application is listening on the correct interface and port.** Inside the container, the application should generally listen on `0.0.0.0` rather than `127.0.0.1` when it needs to accept connections coming from outside the container.

**Step 5: Test connectivity locally** using `curl localhost:<host_port>` on the Docker host and test the container's internal port separately if needed.

**Step 6: Check networking and firewall rules.** I verify the Docker network, security groups, firewall rules, and whether the client is connecting to the correct host IP and port.

**Step 7: Check dependencies and health.** If the application depends on a database or another service, I verify that the dependency is reachable and ready.

Finally, I identify the root cause, apply the fix, and test the application again from the client side.