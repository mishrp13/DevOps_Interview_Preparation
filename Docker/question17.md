```
•EXPOSE vs -p (port publishing)


In a DevOps interview, the key difference is:
- EXPOSE documents which port the application listens on inside the Docker container.
- -p publishes a container port to a port on the Docker host, allowing traffic to reach the container through that host port.
1. EXPOSE vs -p
## EXPOSE vs -p in Docker

| Feature | EXPOSE | -p |
|---|---|---|
| Where used | Dockerfile | `docker run` command |
| Purpose | Documents the container port | Publishes/maps ports |
| Makes app accessible from host? | No, not by itself | Yes, through the published host port |
| Example | `EXPOSE 80` | `-p 8080:80` |
| Required for port publishing? | No | Yes, when using this method |


2. Example with a Dockerfile
Suppose you have a Python web application listening on port 5000.
Dockerfile:

FROM python:3.12-slim

WORKDIR /app
COPY app.py .

RUN pip install flask

EXPOSE 5000

CMD ["python", "app.py"]



Here, EXPOSE 5000 indicates that the application uses port 5000 inside the container.
Important: EXPOSE does not publish that port or automatically make the application accessible from your host machine.
3. Run the container using -p
docker build -t my-python-app .
docker run -d --name my-app -p 8080:5000 my-python-app


The syntax is:
-p HOST_PORT:CONTAINER_PORT


So, -p 8080:5000 means:
- Host port: 8080
- Container port: 5000
Browser / Client
http://localhost:8080

Docker host
Port 8080

Container
Port 5000 — Python application


Now you can access the application at http://localhost:8080, assuming the app is listening correctly and no other networking or firewall issue blocks access.
4. What happens if you use only EXPOSE?
docker run -d --name my-app my-python-app


Even though the Dockerfile contains EXPOSE 5000, Docker does not publish port 5000 to the host.
To publish it, use:
docker run -d -p 5000:5000 my-python-app


You can also publish a different host port:
docker run -d -p 8080:5000 my-python-app


The host and container port numbers do not have to match.
5. What does -P (capital P) mean?
This is a common interview follow-up.
docker run -d -P my-python-app


- -p 8080:5000 — explicitly maps host port 8080 to container port 5000.
- -P — publishes ports declared using EXPOSE to automatically assigned host ports.
To see the published ports:
docker ps
docker port my-app


6. Common DevOps interview questions
Q1. Is EXPOSE mandatory when using -p?
No. You can publish a container port using -p even if the Dockerfile does not contain EXPOSE.
Q2. Does EXPOSE open a firewall port?
No. It does not open a host firewall port or publish the port to the host.
Q3. Can multiple containers use container port 80?
Yes. Each container has its own network namespace. For example:
docker run -d -p 8080:80 nginx
docker run -d -p 8081:80 nginx


Both containers use port 80 internally, but the host uses ports 8080 and 8081.
Q4. What happens if the application listens on 127.0.0.1 inside the container?
Port publishing may not work as expected. The application should generally listen on 0.0.0.0 inside the container so that traffic forwarded to the container can reach it.
Interview-ready answer
“EXPOSE is a Dockerfile instruction that documents the port the application listens on inside the container. It does not publish the port to the host. The -p option is used at runtime to map a host port to a container port, making the application reachable through the published host port. For example, EXPOSE 80 documents port 80, while docker run -p 8080:80 nginx maps host port 8080 to container port 80.”

Easy way to remember: EXPOSE = declare the port; -p = publish the port.