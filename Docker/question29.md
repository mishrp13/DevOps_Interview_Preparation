```
How do you get a shell inside a running container?

To get a shell inside a running Docker container, I use the `docker exec -it` command.

First, I run `docker ps` to identify the container. Then I execute `docker exec -it <container_name> /bin/bash`.

If Bash is unavailable, I use `/bin/sh`, which is common in lightweight images.

Once inside, I can troubleshoot the application by checking files, environment variables, processes, network connectivity, and application logs.

I use `docker exec` because it runs a command inside an existing container without restarting it. If the container is stopped, I first investigate its status and logs because `docker exec` requires a running container.