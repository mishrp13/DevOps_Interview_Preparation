```
•Volumes vs bind mounts vs tmpfs. Why does data disappear when a container is removed?

Here’s an interview-ready answer you can speak directly in a Docker/DevOps interview.
1. Interview question: Volumes vs Bind Mounts vs tmpfs
In Docker, volumes, bind mounts, and tmpfs mounts are used to store data outside the container's writable layer.
1. Volumes: Docker manages the storage. They are used for persistent data, such as database files. The data remains even after the container is removed, as long as the volume is not deleted.
2. Bind mounts: These map a specific host file or directory into the container. They are commonly used for sharing source code, configuration files, and logs between the host and container.
3. tmpfs mounts: These store data in memory instead of persistent container storage. They are useful for temporary files and data that should not persist after the container stops.
The main difference is that volumes are Docker-managed, bind mounts use a specific host path, and tmpfs stores temporary data in memory.




2. Interview question: Why does data disappear when a container is removed?
Docker containers have a writable layer on top of the read-only image layers. When an application writes data inside the container without using a persistent mount, that data is stored in the container's writable layer.
When we remove the container using docker rm, Docker deletes that writable layer, so the data stored there is lost.
To prevent data loss, we use Docker volumes or bind mounts. These store data independently of the container lifecycle.
For example, in production, I would use a Docker volume to persist PostgreSQL database files so that the data remains available even if I recreate the database container.




3. Practical commands to explain in an interview
A. Container writable layer — data is lost on removal
docker run -it --name test ubuntu bash


Inside the container:
echo "Hello" > /data.txt
exit


docker rm test


The file is lost because it was stored only in the container's writable layer.
B. Named volume — data persists
docker volume create mydata

docker run -d --name app \
  --mount source=mydata,target=/data \
  nginx


Remove the container:
docker rm -f app


The named volume mydata remains. A new container can mount the same volume and access its stored data.
C. Bind mount — host files persist
docker run -d --name app \
  --mount type=bind,source=/home/user/app,target=/app \
  nginx


Files remain in /home/user/app on the host even after the container is removed.
D. tmpfs — temporary memory storage
docker run -d --name app \
  --mount type=tmpfs,destination=/tmpdata \
  nginx


The contents of /tmpdata disappear when the container stops or is removed.
4. Common follow-up interview questions

**Docker Interview Questions and Short Answers**

**Q1. Does `docker stop` delete container data?**

Answer: No. The container and its writable layer remain intact. When you start the same container again, its data is still available.

**Q2. Does `docker rm` delete named volumes?**

Answer: Normally, no. Removing a container does not automatically delete its named volumes. The volume remains until it is explicitly removed.

**Q3. Which storage is best for databases?**

Answer: Docker volumes are commonly used for databases because they persist independently of the container lifecycle.

**Q4. Which storage is best for local development?**

Answer: Bind mounts are commonly used to share source code and configuration files between the host and the container.

**Q5. Which storage is temporary and memory-backed?**

Answer: tmpfs. It stores data in memory, and its contents are lost when the container stops or is removed.

**Q6. Is a Docker volume a backup?**

Answer: No. A Docker volume provides persistent storage, but it is not a backup. We must configure separate backups and test data restoration.



Final tip: In a DevOps interview, explain the concept first, demonstrate a command, and then give a real-world example such as PostgreSQL persistence. That shows both theoretical and practical understanding.