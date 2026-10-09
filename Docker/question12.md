```
•Why should you not run containers as root? How do you set a non-root user?

In a DevOps interview, the key point is: You should avoid running containers as root because it increases the security risk if an application is compromised. Run containers with the least privileges necessary.

1. Why should you not run containers as root?

By default, many Docker images run processes as the root user inside the container unless a different user is configured.

Running as root creates several risks:

Privilege escalation: If an attacker exploits a vulnerability in the container, root privileges can make further attacks easier.

Host security risk: Container isolation reduces risk, but it is not an absolute security boundary. A container escape or runtime vulnerability can potentially expose the host.

File permission issues: Applications may create files owned by root, causing permission problems for other users or processes.

Excessive privileges: The application receives more permissions than it usually needs, violating the principle of least privilege.

Important interview point: Root inside a container is not automatically root on the host. Docker provides isolation, but running as root increases the potential impact of a container breakout.

2. How do you set a non-root user in Docker?

You can use the USER instruction in your Dockerfile.

Example: Run a Python application as a non-root user
FROM python:3.12-slim

# Create a dedicated application user
RUN useradd --create-home appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Switch from root to a non-root user
USER appuser

CMD ["python", "app.py"]

How this works:

FROM selects the base image.

RUN useradd --create-home appuser creates a dedicated user.

Dependencies and application files are prepared.

USER appuser makes subsequent Dockerfile instructions that run as a user, including the default application process, use appuser rather than root.

CMD starts the application.

Note: Files copied into an image are not automatically owned by appuser. If the application needs to write to a directory, set the appropriate ownership or permissions during the build.

For example:

RUN mkdir -p /app/data \
    && chown -R appuser:appuser /app/data

Place this command before USER appuser so the build can set the permissions.

3. How do you verify that the container is not running as root?

Build and run the image:

docker build -t secure-python-app .
docker run -d --name test-app secure-python-app

Check the running process's user:

docker exec test-app whoami

Expected output:

appuser

You can also inspect the configured user:

docker image inspect secure-python-app \
  --format '{{.Config.User}}'

Expected output:

appuser

The image inspection command shows the configured user; checking a running process confirms the actual runtime identity.

4. Alternative: Specify the user at runtime

You can override the image's configured user with the --user flag:

docker run --user 1001:1001 myapp

Here, 1001 is the UID and the second 1001 is the GID.

This is useful when your deployment environment requires a specific user ID. However, ensure that the application has the necessary file and directory permissions.

5. Best practices for DevOps and production
Best practice                                         Why it matters

Use USER in the Dockerfile      -> Makes non-root execution the image default.

Apply least privilege  -->   Gives the application only the permissions it needs.


Use COPY --chown where appropriate  -> Avoids unnecessary ownership changes in later layers.


Avoid unnecessary Linux capabilities  -> Reduces what a compromised process can do.

Use a read-only filesystem when practical --> Prevents unintended writes to the container filesystem.

Scan images and keep dependencies updated  --> Reduces exposure to known vulnerabilities

Configure Kubernetes security contexts  --> Enforces non-root execution and other runtime restrictions.


For example, in Kubernetes you can enforce non-root execution with a pod security context:

spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    runAsGroup: 1001

The image must be compatible with that UID and have the necessary permissions.

6. Common DevOps interview questions

Q1. Does running as a non-root user make a container completely secure?

No. It reduces risk, but you still need proper isolation, limited capabilities, secure configurations, updated images, and runtime security controls.

Q2. What happens if you don't specify USER in a Dockerfile?

The process generally runs as root if the base image does not specify another user. Some images already configure a non-root user, so check the base image.

Q3. What if my application needs port 80?

On traditional Linux configurations, binding to port 80 normally requires elevated privileges or the relevant capability. Prefer running the application on an unprivileged port such as 8080 and configure the host or orchestrator to expose port 80 externally. Avoid running the entire application as root just to bind a port.

Q4. What is the difference between USER and --user?

USER sets the default user in the Docker image.

docker run --user overrides that default for a particular container.

7. Interview answer to memorize
Writing

We should avoid running Docker containers as root because it violates the principle of least privilege and can increase the impact of a security breach.

If an attacker compromises an application running as root, they may have more opportunities to exploit container or host vulnerabilities. Running as a non-root user reduces unnecessary privileges.

To implement this, I create a dedicated application user in the Dockerfile and switch to it using the USER instruction before starting the application. I also ensure the application files and required directories have the correct permissions.

In production, I combine non-root execution with security measures such as dropping unnecessary Linux capabilities, using read-only filesystems where practical, scanning images, and enforcing security contexts in Kubernetes.

Quick revision: Create user → Set permissions → Add USER instruction → Verify at runtime.