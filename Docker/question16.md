```
•Bridge, host and none network modes. How do containers talk to each other?


In a DevOps interview, Docker networking explains how containers communicate with each other, the host machine, and external networks.

The three main Docker network modes you should know are:

Bridge: Containers communicate over a Docker-managed network.

Host: The container shares the host's network namespace.

None: The container has no normal network connectivity, apart from its loopback interface.

1. Bridge, host, and none network modes

1. Bridge network — default for standalone containers

Most common

Docker connects containers to a virtual bridge network. Containers on the same user-defined bridge can communicate using container names as DNS names.

Example:

docker network create mynet

docker run -d --name app \
  --network mynet nginx

docker run -it --rm \
  --network mynet busybox sh

From the BusyBox container, you can test connectivity to the app using wget -qO- http://app.

Use case: Web application and database containers communicating privately.

2. Host network

The container shares the host's network namespace on supported Linux setups. It does not receive a separate container network namespace.

docker run -d \
  --network host \
  nginx

Nginx listens directly on the host's network interfaces using its configured port. You do not need -p port publishing in host mode.

Use case: Specialized workloads where avoiding Docker's separate network namespace or port publishing is useful.

Limitation: Port conflicts are possible, and network isolation is reduced.

3. None network

Docker does not attach the container to a normal network. The container retains its loopback interface, but it has no normal external or inter-container network connectivity.

docker run -d \
  --network none \
  --name isolated-app \
  nginx

Use case: Isolated batch jobs, security-sensitive processing, or workloads that do not need network access.

2. Quick comparison table
| Feature                 | Bridge                                      | Host                                 | None                                 |
| ----------------------- | ------------------------------------------- | ------------------------------------ | ------------------------------------ |
| Network                 | Private Docker network                      | Shares host network                  | No external network                  |
| IP address              | Separate container IP                       | Uses host network                    | Loopback only                        |
| Port mapping (`-p`)     | Required for host access                    | Not required                         | Not applicable                       |
| Container communication | Yes, on the same network                    | Through host networking              | No normal network communication      |
| Isolation               | Good                                        | Low                                  | Strong network isolation             |
| DNS by container name   | Yes, on user-defined bridge                 | Not provided by bridge networking    | No                                   |
| Common use case         | Most applications                           | Performance-sensitive networking     | Isolated workloads                   |
| Example                 | `docker run -d --name app -p 8080:80 nginx` | `docker run -d --network host nginx` | `docker run -d --network none nginx` |


3. How do containers talk to each other?

This is one of the most important follow-up questions in a DevOps interview.

Imagine you have a three-tier application:

Frontend: React or Nginx

Backend: Node.js or Java

Database: MySQL

Frontend container

Nginx — port 80

HTTP request to http://backend:8080

Backend container

Node.js — port 8080

Database connection to db:3306

Database container

MySQL — port 3306

All three containers are attached to the same user-defined bridge network.

Step 1: Create a shared network
docker network create app-network
Step 2: Start the database
docker run -d \
  --name db \
  --network app-network \
  -e MYSQL_ROOT_PASSWORD=example \
  mysql:8

For real deployments, use a securely managed password rather than putting credentials directly in commands.

Step 3: Start the backend
docker run -d \
  --name backend \
  --network app-network \
  my-backend:1.0

Configure the backend to connect to the database using hostname db and port 3306.

Step 4: Start the frontend
docker run -d \
  --name frontend \
  --network app-network \
  -p 8080:80 \
  nginx

The frontend can be accessed from the host at http://localhost:8080.

The key distinction is:

Container-to-container: Use the container or service name and its listening port, such as db:3306.

Host-to-container: Use a published host port, such as localhost:8080.

Container-to-external service: Use the destination's reachable hostname or IP, subject to routing and firewall rules.

A frontend container does not automatically make backend resolvable inside a user's browser. If browser-side JavaScript calls the backend, you need an externally reachable backend URL or a reverse proxy.

4. What if containers are on different networks?

Containers attached to different isolated bridge networks cannot normally communicate directly through Docker's network-name DNS.

You can attach a container to another network:

docker network connect app-network backend

Once the containers share a user-defined bridge network, they can communicate using their container names, assuming the application is listening on the appropriate interface and port.

5. Common DevOps interview questions

Q1. What is the difference between the default bridge and a user-defined bridge?

A user-defined bridge provides automatic DNS resolution between containers by name and offers more flexible network configuration. The default bridge has more limited name-based discovery and traditionally relies on IP addresses or legacy linking.

Q2. Do containers need -p to communicate with each other?

No. Containers on the same user-defined bridge network can communicate directly over their container ports. Use -p when you need to publish a container port to the host or make it accessible through that host port.

Q3. Why would you use host networking?

For specialized workloads that benefit from sharing the host network namespace. However, it reduces network isolation and can cause port conflicts.

Q4. Can containers communicate in none mode?

Not through normal Docker networking. The container retains loopback connectivity, but it has no normal network attachment.

Q5. How do you troubleshoot Docker networking issues?

docker network ls
docker network inspect app-network
docker inspect backend
docker logs backend

Then verify DNS resolution, connectivity, application listening ports, network membership, and firewall rules.

6. Interview answer to memorize
Writing

Docker supports different network modes, including bridge, host, and none.

In bridge mode, containers connect through a Docker-managed virtual network. I prefer a user-defined bridge network because containers can communicate using their names through Docker's built-in DNS.

In host mode, the container shares the host's network namespace, so port publishing is not required, but network isolation is reduced.

In none mode, the container has no normal network connectivity and is useful for isolated workloads.

For container-to-container communication, I place related containers on the same user-defined bridge network and use their container names and listening ports. For example, a backend can connect to a database using db:3306. I use port publishing with -p when external clients need to access a container through the host.

Quick revision: Bridge = shared virtual network; Host = shares host networking; None = no normal network. For application containers, a user-defined bridge is a common starting point.