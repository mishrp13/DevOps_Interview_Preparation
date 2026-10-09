```
•What is a multi-stage build? Why use it?

In a DevOps interview, a Docker multi-stage build is a technique where you use multiple FROM statements in a single Dockerfile to build an application in one stage and copy only the required artifacts into the final image.

The main purpose is to reduce Docker image size, improve security, and keep production images clean.

1. What is a multi-stage build?

Normally, building an application may require compilers, build tools, dependencies, and source code. But in production, you often need only the final executable or application files.

Multi-stage builds solve this problem by separating the build environment from the runtime environment.

Stage 1: Builder

Contains source code, compiler, build tools, and dependencies.

Example: Compile a Java application using Maven.

COPY only the required artifact

Stage 2: Production

Contains the compiled application and only the runtime requirements.

Example: A JRE and the application JAR file.

Final Docker image

Smaller, cleaner, and with fewer unnecessary tools.

2. Example: Docker multi-stage build

Suppose you are building a Java application using Maven.

Without a multi-stage build

You might use a Maven image that contains build tools in the final image, even though production only needs to run the JAR file.

With a multi-stage build
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

COPY pom.xml .
COPY src ./src

RUN mvn clean package -DskipTests

# Stage 2: Run the application
FROM eclipse-temurin:17-jre

WORKDIR /app

COPY --from=builder /app/target/*.jar app.jar

CMD ["java", "-jar", "app.jar"]

What is happening here?

FROM ... AS builder creates the build stage with Maven and the JDK.

RUN mvn clean package compiles the application and generates a JAR.

The second FROM starts a separate final image stage.

COPY --from=builder copies the JAR from the builder stage into the runtime image.

CMD runs the application when the container starts.

Build and run it:

docker build -t my-java-app .
docker run -p 8080:8080 my-java-app

The final image does not include Maven or the source code copied into the builder stage, unless you explicitly copy them.

3. Why do we use multi-stage builds?

Benefit                                                  Explanation
Smaller image size                                Build tools and unnecessary files are excluded from the final image.
Better security                                      Fewer unnecessary utilities and tools are available in production.
Faster deployments                              Smaller images can be quicker to transfer and distribute.
Cleaner production environment           Keeps compilers, source code, and build dependencies out of the runtime image.
Better CI/CD pipelines                         Builds and packages applications consistently within a Dockerfile.
Easier maintenance                                   Separates build instructions from runtime configuration.


Note: Multi-stage builds can improve image size and security, but the actual benefit depends on the base images, dependencies, and files copied into the final stage.

4. Important Docker commands
# Build the Docker image
docker build -t myapp:latest .

# View local images and their sizes
docker images

# Build only a specific stage
docker build --target builder -t myapp-builder .

The --target option is useful when you want to build a particular stage, such as the builder stage, for debugging or testing.

5. Common DevOps interview questions

Q1. What is the difference between a normal Docker build and a multi-stage build?

A normal single-stage build typically uses one base image for both building and running the application. A multi-stage build uses separate stages and copies only the required artifacts into the final image.

Q2. Can we use more than two stages?

Yes. You can use multiple stages, such as:

Stage 1: Install dependencies.

Stage 2: Build the application.

Stage 3: Run automated tests.

Stage 4: Create the production image.

Each stage can use a different base image.

Q3. Does Docker include all stages in the final image?

No. The final image contains the final stage and the files explicitly copied into it from earlier stages. Earlier stages may be used during the build without being included in the final image.

Q4. How does a multi-stage build improve security?

It reduces the attack surface by excluding unnecessary build tools, compilers, and other utilities from the production image. It does not automatically guarantee security; you still need secure base images, dependency management, and vulnerability scanning.

Q5. What does COPY --from=builder mean?

It copies files from a previously defined build stage named builder into the current stage.

For example:

COPY --from=builder /app/target/app.jar /app/app.jar

This copies the JAR file from the builder stage to the destination in the current image.

6. Best interview answer to memorize
Writing

A multi-stage build in Docker is a technique in which we use multiple FROM instructions in a single Dockerfile to separate the build environment from the runtime environment.

For example, when building a Java application, the first stage uses Maven and the JDK to compile the source code and generate a JAR file. The second stage uses a lightweight Java runtime image and copies only the JAR file from the builder stage using COPY --from=builder.

We use multi-stage builds to reduce Docker image size, improve security by removing unnecessary build tools, speed up image distribution, and keep production containers clean.

In a DevOps CI/CD pipeline, multi-stage builds help us create optimized production images that are easier to deploy and maintain.

Remember for your interview: The key concept is build in one stage, copy the required artifacts, and run in another stage.