```
The disk is full on a Docker host. How do you clean up? (docker system prune, dangling images, old volumes)

If the Docker host disk is full, I would first run `df -h` to identify the full filesystem and `docker system df -v` to understand Docker's disk usage.

Then I would inspect the resources and remove unnecessary items in a controlled way. I would use `docker container prune` for stopped containers, `docker image prune` for dangling images, `docker builder prune` for build cache, and `docker network prune` for unused networks.

If more space is required, I would consider `docker image prune -a` to remove unused images and `docker system prune` for general cleanup.

I would be especially careful with volumes because they can contain persistent application or database data. Before removing volumes, I would verify that they are no longer required and that important data is backed up.

Finally, I would rerun `df -h` and `docker system df` to verify the recovered space. In production, I would also investigate why the disk filled up and set up disk-usage monitoring and log rotation to prevent recurrence.