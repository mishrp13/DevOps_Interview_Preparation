```

•What is Docker Compose? Write a compose file for an app plus a database

1. What is Docker Compose?
Interview answer (copy-ready):

Docker Compose is a tool used to define and manage multi-container Docker applications using a YAML configuration file called `compose.yaml` or `docker-compose.yml`.

Instead of running multiple `docker run` commands separately, we define all services, networks, volumes, environment variables, and dependencies in one file.

For example, an application may require two containers:
1. An application container running the backend.
2. A database container running MySQL.

Using Docker Compose, we can start, stop, and manage both containers with a single command.

Docker Compose is commonly used in local development, testing, and DevOps workflows. It simplifies application deployment and makes the environment easier to reproduce.

2. Example: App + Database using Docker Compose
Imagine a project with:
- App: A backend application running on port 3000.
- Database: MySQL running on port 3306.
- Volume: Stores database data persistently.
- Network: Allows the app to communicate with the database.



Compose file
Create a file named compose.yaml:


services:
  app:
    image: myapp:latest
    ports:
      - "3000:3000"
    environment:
      DB_HOST: db
      DB_PORT: "3306"
      DB_NAME: appdb
      DB_USER: appuser
      DB_PASSWORD: ${DB_PASSWORD}
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:8.4
    environment:
      MYSQL_DATABASE: appdb
      MYSQL_USER: appuser
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
      interval: 10s
      timeout: 5s
      retries: 10

volumes:
  db_data:


Create a .env file in the same directory:

DB_PASSWORD=change_this_app_password
DB_ROOT_PASSWORD=change_this_root_password


These are example credentials; use strong credentials and a proper secrets-management solution outside local testing. Do not commit .env files containing real secrets to Git.
Important: myapp:latest represents your own application image. Replace it with the actual image for your application. The application must support the specified database environment variables and connect to MySQL.



3. Explain each section in an interview
C**Docker Compose Keys and Their Explanations**

**1. `services`**  
Defines the containers or services that make up the application.

**2. `app`**  
Defines the backend application service.

**3. `db`**  
Defines the MySQL database service.

**4. `image`**  
Specifies the Docker image used to create the container.

**5. `ports`**  
Maps a host port to a container port.

**6. `environment`**  
Passes configuration variables and database credentials into a container.

**7. `depends_on`**  
Controls service startup order. With `condition: service_healthy`, Compose waits for the dependency's health check to pass.

**8. `healthcheck`**  
Checks whether the database is healthy and ready to accept connections.

**9. `volumes`**  
Persists database files outside the container's writable layer so the data survives container recreation.

**10. `db_data`**  
A named Docker volume managed by Docker to store persistent database data.




How does the app connect to the database?
Inside the Compose network, the application connects to:
DB_HOST=db
DB_PORT=3306


Here, db is the Compose service name, which Docker's internal DNS resolves to the database container.
Interview tip: The app normally uses db:3306, not localhost:3306. Inside a container, localhost refers to that same container.

4. Docker Compose commands
Run these commands from the directory containing compose.yaml.


# Validate the Compose configuration
docker compose config

# Build the app image and start services
docker compose up -d --build

# List services and their status
docker compose ps

# View logs
docker compose logs -f

# View only application logs
docker compose logs -f app

# Stop and remove containers and network
docker compose down

# Stop and remove containers, network, and named volumes
docker compose down -v

Be careful with docker compose down -v: it removes the Compose-managed named volume, including the stored database data, when that volume is eligible for removal.
5. Common DevOps interview follow-up questions
Q1. What is the difference between Docker and Docker Compose?
Answer: Docker provides the platform and commands to build and run containers. Docker Compose defines and manages a multi-container application through a YAML configuration file.


Q2. Why do we use depends_on?
Answer: It defines service dependencies and can control startup order. By itself, it does not guarantee that a database is ready. Using condition: service_healthy with a health check lets Compose wait for the database health check to pass.


Q3. Why do we use volumes in Docker Compose?
Answer: Volumes persist important data outside the container's writable layer. For example, MySQL stores its database files in the db_data volume so the data survives ordinary container recreation.


Q4. How do containers communicate in Compose?
Answer: Compose creates a default network for the application. Services can communicate using their service names, such as app and db, and the destination container port.


Q5. What happens when you run docker compose down?
Answer: Compose stops and removes the project's containers and its default network. Named volumes are normally preserved unless you specify -v or remove them separately.


Q6. Is Docker Compose used in production?
Answer: Yes, it can be used for production deployments on suitable single-host environments. For larger distributed applications requiring orchestration across multiple machines, teams may use Kubernetes or another orchestration platform.


6. Best short answer to memorize


Docker Compose is a tool for defining and managing multi-container applications using a YAML file. For example, I can define an application service and a MySQL database service in compose.yaml, configure environment variables, connect them through a Docker network, and persist database data using a named volume.
I use docker compose up -d to start the application, docker compose logs to troubleshoot it, and docker compose down to stop and remove its containers and network. Compose simplifies development, testing, and deployment by keeping the application configuration in one place.