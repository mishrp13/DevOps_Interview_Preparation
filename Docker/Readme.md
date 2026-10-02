
```

1. Simple Java application

Imagine this project:

java-docker-demo/
├── src/
│   └── Main.java
└── Dockerfile

Main.java:

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Java Docker!");
    }
}
2. Normal Dockerfile

A single-stage Dockerfile does everything in one image: it contains the JDK, source code, compiler, compiled .class files, and runtime.

FROM eclipse-temurin:17-jdk

WORKDIR /app

COPY src/Main.java .

RUN javac Main.java

CMD ["java", "Main"]
Understand every line
FROM eclipse-temurin:17-jdk

Starts from a Java 17 JDK image.

Why JDK?

Because we need javac to compile Java code.

WORKDIR /app

Sets /app as the working directory inside the container.

So commands are effectively executed from:

/app
COPY src/Main.java .

Copies our Java source file into /app.

Inside the container:

/app/Main.java
RUN javac Main.java

Compiles:

Main.java
    ↓
Main.class

This happens when the Docker image is built.

CMD ["java", "Main"]

This is the default command executed when the container starts.

So:

docker build
     ↓
javac Main.java
     ↓
Main.class
     ↓
docker run
     ↓
java Main
3. Build and run it

From the project directory:

docker build -t java-demo .

Then:

docker run java-demo

Output:

Hello from Java Docker!
Interview question

Q: What is the difference between RUN and CMD?

A good answer:

RUN executes a command while building the Docker image and creates a new image layer. CMD defines the default command that runs when a container starts.

That's a very common interview question.

4. Multi-stage Dockerfile

Now we improve the previous Dockerfile.

The idea is:

Build the application using a JDK, then run it using a smaller JRE/runtime image.

# Stage 1: Build
FROM eclipse-temurin:17-jdk AS builder

WORKDIR /app

COPY src/Main.java .

RUN javac Main.java


# Stage 2: Run
FROM eclipse-temurin:17-jre

WORKDIR /app

COPY --from=builder /app/Main.class .

CMD ["java", "Main"]

This is called a multi-stage build.

5. Understand the two stages
Stage 1 — Builder
FROM eclipse-temurin:17-jdk AS builder

We use the JDK because we need the Java compiler.

Main.java
   ↓
javac
   ↓
Main.class
Stage 2 — Runtime
FROM eclipse-temurin:17-jre

We don't need the compiler anymore.

We only need to execute:

java Main

So we use the JRE/runtime image.

Then:

COPY --from=builder /app/Main.class .

This is the important line.

It says:

Copy Main.class from the builder stage into the final image.

The final image doesn't need:

Main.java
javac
full JDK
build tools

It only needs the compiled application and Java runtime.

6. Why do companies use multi-stage Docker builds?

This is the answer I'd give in an interview:

Multi-stage Docker builds separate the build environment from the runtime environment. We can use a larger JDK image to compile the application and then copy only the required artifacts into a smaller runtime image. This reduces the final image size, improves security by removing unnecessary build tools, and keeps the production image cleaner.

Remember this:
Single stage

JDK
+ source code
+ compiler
+ application
        ↓
     BIG IMAGE

Multi-stage:

          BUILD STAGE
              |
              | JDK
              | source
              | compiler
              ↓
         Main.class
              |
              ↓
        RUNTIME STAGE
              |
              | JRE
              | Main.class
              ↓
        SMALLER IMAGE
7. Build the multi-stage image
docker build -t java-demo:multi .

Run it:

docker run java-demo:multi

Output:

Hello from Java Docker!

The important thing is that only the final stage becomes the resulting image.

8. Now Docker Compose

Docker Compose is useful when your application consists of multiple containers/services.

For example:

Java application
       |
       ↓
    Database

Instead of manually running:

docker network ...
docker run ...
docker run ...

we can define everything in a compose.yaml file.

9. Simple Docker Compose example

Let's say our Java application needs MySQL.

Project:

java-docker-demo/
├── src/
│   └── Main.java
├── Dockerfile
└── compose.yaml

compose.yaml:

services:

  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: java-app
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    container_name: mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: demo
    ports:
      - "3306:3306"

Then start everything:

docker compose up --build
10. Understand the Compose file
services
services:

Defines the containers/services that make up our application.

Here we have:

app
mysql
Java application
app:
  build:
    context: .
    dockerfile: Dockerfile

This tells Compose:

Build my Java application's Docker image using the Dockerfile in the current directory.

depends_on
depends_on:
  - mysql

Means the application has a dependency on the MySQL service.

MySQL
mysql:
  image: mysql:8.0

Instead of building MySQL ourselves, Docker pulls an existing MySQL image.

Environment variables
environment:
  MYSQL_ROOT_PASSWORD: root
  MYSQL_DATABASE: demo

These configure MySQL.

In a real production environment, don't hard-code passwords like this. Use secrets/environment management.

Ports
ports:
  - "3306:3306"

This means:

Host port 3306
       ↓
Container port 3306

So you can connect to MySQL from your host on port 3306.

11. Very important Docker Compose interview concept

Suppose your Java application connects to MySQL.

Inside Compose, don't use localhost to connect to MySQL.

Wrong:

localhost:3306

Use the service name:

mysql:3306

Why?

Because Compose creates a network for the services, and Docker's internal DNS allows the service name to resolve to the appropriate container.

So:

Java container
      |
      | mysql:3306
      ↓
MySQL container

This is an extremely useful interview point.

12. Most important commands to remember
Build an image
docker build -t java-app .
Run a container
docker run java-app
See running containers
docker ps
See all containers
docker ps -a
Stop a container
docker stop <container>
Remove a container
docker rm <container>
List images
docker images
Start Compose
docker compose up
Build and start
docker compose up --build
Run in background
docker compose up -d
Stop Compose
docker compose down
View logs
docker compose logs

Or:

docker compose logs app
13. Interview questions you should practice tonight
Q1. What is Docker?

Docker is a containerization platform that packages an application along with its dependencies into a container so that it can run consistently across different environments.

Q2. What is a Docker image?

A Docker image is a read-only template containing the application, dependencies, libraries, and instructions required to create a container.

Q3. What is a container?

A container is a running instance of a Docker image.

Easy way to remember:

Image → blueprint
Container → running instance
Q4. What is a Dockerfile?

A Dockerfile is a text file containing instructions used to build a Docker image.

Q5. What is a multi-stage build?

A multi-stage build uses multiple FROM statements. Typically, one stage builds the application using development tools, while a later stage contains only the artifacts required to run it.

Q6. Why use multi-stage builds?

Say these three things:

Smaller image + better security + cleaner production image.

Q7. What is Docker Compose?

Docker Compose is a tool for defining and running multi-container applications using a YAML configuration file.

Q8. Dockerfile vs Docker Compose?

This is important.

Dockerfile	Docker Compose
Builds an image	Runs/manages services
Defines image contents	Defines application services
Uses Dockerfile syntax	Uses YAML
Usually one application image	Can manage multiple containers

Think:

Dockerfile
    ↓
How do I BUILD my application image?

Compose
    ↓
How do I RUN my application and its dependencies?
14. One thing to memorize for tomorrow

If the interviewer asks:

"Explain how you containerized a Java application."

You can say:

"I created a Dockerfile using a Java 17 JDK image. I set the working directory, copied the Java source code, compiled it using javac, and configured the application to run using java. Then I improved it using a multi-stage Docker build. In the first stage I used the JDK to compile the application, and in the second stage I used a smaller Java runtime image and copied only the compiled artifact from the builder stage. This reduces the final image size and removes unnecessary build tools. For multi-container environments, I use Docker Compose to define services such as the Java application and MySQL, configure their environment variables, networking, dependencies, and ports."

That's a solid 1–2 minute interview answer.

Your mental picture

Memorize this:

              Dockerfile
                  |
                  ↓
             docker build
                  |
                  ↓
             Docker Image
                  |
                  ↓
             docker run
                  |
                  ↓
              Container


          Multi-stage build

       JDK / BUILD IMAGE
              |
       compile Java code
              |
              ↓
          .class / JAR
              |
              ↓
       JRE / RUNTIME IMAGE
              |
              ↓
       Smaller production image


             Docker Compose

       ┌─────────────────┐
       │   Java App      │
       │   Container     │
       └────────┬────────┘
                │
                │ mysql:3306
                ↓
       ┌─────────────────┐
       │     MySQL       │
       │   Container     │
       └─────────────────┘

If you remember that picture, you can reconstruct most of the syntax instead of trying to memorize everything.


```