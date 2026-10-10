```
A container exits immediately. How do you debug? (docker logs, docker inspect, exit codes)

If a Docker container exits immediately, I follow a systematic troubleshooting approach.

**Step 1: Check the container status.** I use `docker ps -a` to confirm whether the container has exited and to check its exit code.

**Step 2: Check the container logs.** I use `docker logs <container_name>` to identify application errors, missing configuration, database connection failures, or other startup issues.

**Step 3: Inspect the container.** I use `docker inspect <container_name>` to check the exit code, error message, environment configuration, entrypoint, command, and other container settings.

**Step 4: Analyze the exit code.** Exit code 0 generally indicates successful completion, while a non-zero exit code indicates an error. Exit code 137 often indicates that the process was killed with SIGKILL, sometimes because of an out-of-memory event.

**Step 5: Check the application command.** Containers stop when their main process finishes or exits. I verify the Dockerfile's `CMD` and `ENTRYPOINT` and confirm that the application is running in the foreground.

**Step 6: Fix the root cause.** After identifying the issue, I correct the configuration, command, dependency, or resource problem and recreate or restart the container as appropriate.

I also verify the fix by checking the container status and reviewing the logs again.