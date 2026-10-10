```
•What is the difference between docker run, docker start and docker exec?

**1. docker run:** Creates a new container from an image and starts it. If the image is not available locally, Docker may pull it from a registry.

**2. docker start:** Starts an existing stopped container. It does not create a new container.

**3. docker exec:** Executes a command inside an already running container without creating another container.

In DevOps, I use `docker run` to create and launch a new container, `docker start` to restart an existing stopped container, and `docker exec` to troubleshoot a running container or execute commands inside it.

1. docker run — Create + Start

docker run -d --name myapp nginx

2.docker start — Start Existing Container

docker stop myapp
docker start myapp

3. docker exec — Execute Inside Running Container

docker exec -it myapp bash