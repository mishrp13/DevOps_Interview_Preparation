```
How do you persist logs from a container?

To persist Docker container logs, I first identify whether the application writes logs to standard output and standard error or to files.

For applications that write to standard output and standard error, I use Docker's logging drivers and inspect logs with `docker logs`. I also configure log rotation to prevent logs from consuming all the host's disk space.

If the application writes logs to files, I mount a Docker volume or bind mount so those files survive container replacement.

In production, I prefer centralized logging solutions such as the ELK Stack, Fluent Bit with Loki, or a cloud logging service. This allows us to collect, search, monitor, and retain logs across multiple containers and hosts.

Finally, I configure retention policies, monitor disk usage, and verify that logs are actually reaching the destination.

