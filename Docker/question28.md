```
How do you limit CPU and memory for a container?

In Docker, I can control container resource usage by setting CPU and memory limits.

For example, I can run a container with `--cpus="1.0"` and `--memory="512m"` to limit it to one CPU's worth of processing time and 512 MB of memory.

CPU limits help prevent one container from monopolizing CPU resources, while memory limits protect the host from excessive memory consumption. If a container exceeds its memory limit, it may experience an OOM kill.

In Docker Compose, I can configure these limits in the service definition. I would monitor actual usage with `docker stats` and adjust the limits based on the application's workload.

This helps improve resource isolation, host stability, and predictable performance across multiple containers.