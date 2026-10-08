```

Absolutely. For a DevOps/AWS/Kubernetes interview, this is the kind of Spring Boot Dockerfile I'd present. It demonstrates multi-stage builds, Maven caching, small runtime image, non-root execution, health checks, JVM container awareness, and clean separation between build and runtime.

Production-style Spring Boot Dockerfile
Production Spring Boot Multi-Stage Dockerfile
# syntax=docker/dockerfile:1

############################
# 1. Build Stage
############################
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

# Copy Maven wrapper and dependency files first
# This allows Docker to cache dependencies
COPY .mvn/ .mvn/
COPY mvnw pom.xml ./

RUN chmod +x mvnw

# Download dependencies
RUN --mount=type=cache,target=/root/.m2 \
    ./mvnw dependency:go-offline -B

# Copy source code only after dependencies
COPY src ./src

# Build the application
RUN --mount=type=cache,target=/root/.m2 \
    ./mvnw clean package -DskipTests


############################
# 2. Extract Application Layers
############################
FROM eclipse-temurin:21-jdk-alpine AS extractor

WORKDIR /app

COPY --from=builder /app/target/*.jar app.jar

# Extract Spring Boot layered JAR
RUN java -Djarmode=tools \
    -jar app.jar extract --layers --launcher


############################
# 3. Production Runtime
############################
FROM eclipse-temurin:21-jre-alpine AS runtime

WORKDIR /app

# Create non-root user
RUN addgroup -S spring && \
    adduser -S spring -G spring

# Copy Spring Boot layers separately
COPY --from=extractor /app/app/dependencies/ ./
COPY --from=extractor /app/app/spring-boot-loader/ ./
COPY --from=extractor /app/app/snapshot-dependencies/ ./
COPY --from=extractor /app/app/application/ ./

# Security: run application as non-root
USER spring:spring

# JVM configuration
ENV JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=75.0 \
-Djava.security.egd=file:/dev/./urandom"

# Spring Boot default port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s \
            --timeout=5s \
            --start-period=30s \
            --retries=3 \
            CMD wget --no-verbose \
                --tries=1 \
                --spider \
                http://127.0.0.1:8080/actuator/health \
                || exit 1

# Start Spring Boot application
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
.dockerignore
.git
.gitignore
.idea
.vscode

target
*.log

Dockerfile
.dockerignore

README.md

.env
.env.*
The interview explanation

The impressive part isn't just showing the Dockerfile. Explain why you designed it this way:

“I use three stages here: a builder stage, an extraction stage, and a minimal JRE runtime stage. The builder uses the JDK because Maven needs the full Java toolchain, while the runtime only needs the JRE. I copy pom.xml before the source code so Maven dependency layers can be cached. I also use BuildKit cache mounts for Maven dependencies to make subsequent builds faster.”

Then:

“For Spring Boot specifically, I use layered JARs. That allows Docker to cache relatively stable dependency layers separately from frequently changing application code, so a small source-code change doesn't force Docker to rebuild the entire image.”

Then hit the security point:

“I don't run the application as root. The runtime image creates a dedicated spring user and switches to it with USER.”

And finally:

“The JVM is container-aware, and I use MaxRAMPercentage rather than hardcoding a heap size because the container memory limit can vary between environments such as Docker, ECS, or Kubernetes.”

If they ask: "Why not just use one FROM?"

Say:

“A single-stage image would contain the JDK, Maven build tooling, source/build files and other artifacts that aren't required at runtime. With multi-stage builds, I can use a full JDK in the build environment but ship only the JRE and application layers in production. That reduces image size and attack surface.”

If they ask about Kubernetes

This Dockerfile also gives you a nice bridge into Kubernetes:

Developer
   │
   ▼
Docker Build
   │
   ├── Builder → JDK + Maven
   │
   ├── Extractor → Spring Boot layers
   │
   ▼
Runtime Image
   │
   ├── JRE only
   ├── Non-root user
   ├── Health check
   └── JVM container configuration
   │
   ▼
Container Registry
   │
   ▼
Kubernetes / ECS

One important interview nuance: in Kubernetes, I'd normally prefer Kubernetes startupProbe, readinessProbe, and livenessProbe for orchestration-level health management rather than relying solely on Docker's HEALTHCHECK. Mentioning that distinction will make your answer stronger.

Also, if the interviewer asks you to improve this further, mention image scanning, SBOM generation, pinned base-image digests, read-only root filesystems, dropped Linux capabilities, and running with a non-root UID. Those are excellent follow-up topics for a DevOps interview.

The interview explanation

The impressive part isn't just showing the Dockerfile. Explain why you designed it this way:

“I use three stages here: a builder stage, an extraction stage, and a minimal JRE runtime stage. The builder uses the JDK because Maven needs the full Java toolchain, while the runtime only needs the JRE. I copy pom.xml before the source code so Maven dependency layers can be cached. I also use BuildKit cache mounts for Maven dependencies to make subsequent builds faster.”

Then:

“For Spring Boot specifically, I use layered JARs. That allows Docker to cache relatively stable dependency layers separately from frequently changing application code, so a small source-code change doesn't force Docker to rebuild the entire image.”

Then hit the security point:

“I don't run the application as root. The runtime image creates a dedicated spring user and switches to it with USER.”

And finally:

“The JVM is container-aware, and I use MaxRAMPercentage rather than hardcoding a heap size because the container memory limit can vary between environments such as Docker, ECS, or Kubernetes.”

If they ask: "Why not just use one FROM?"

Say:

“A single-stage image would contain the JDK, Maven build tooling, source/build files and other artifacts that aren't required at runtime. With multi-stage builds, I can use a full JDK in the build environment but ship only the JRE and application layers in production. That reduces image size and attack surface.”

If they ask about Kubernetes

This Dockerfile also gives you a nice bridge into Kubernetes:

Developer
   │
   ▼
Docker Build
   │
   ├── Builder → JDK + Maven
   │
   ├── Extractor → Spring Boot layers
   │
   ▼
Runtime Image
   │
   ├── JRE only
   ├── Non-root user
   ├── Health check
   └── JVM container configuration
   │
   ▼
Container Registry
   │
   ▼
Kubernetes / ECS

One important interview nuance: in Kubernetes, I'd normally prefer Kubernetes startupProbe, readinessProbe, and livenessProbe for orchestration-level health management rather than relying solely on Docker's HEALTHCHECK. Mentioning that distinction will make your answer stronger.

Also, if the interviewer asks you to improve this further, mention image scanning, SBOM generation, pinned base-image digests, read-only root filesystems, dropped Linux capabilities, and running with a non-root UID. Those are excellent follow-up topics for a DevOps interview.