```
•What is a Dockerfile? Explain the main instructions (FROM, RUN, COPY, CMD, ENTRYPOINT, ENV, EXPOSE, WORKDIR)

For a DevOps interview, understand a Dockerfile as the recipe used to build a container image.

1. What is a Dockerfile?

A Dockerfile is a text file containing instructions that Docker uses to build a container image.

Example:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV APP_ENV=production

EXPOSE 8000

CMD ["python", "app.py"]

When you run:

docker build -t myapp:1.0 .

Docker reads the Dockerfile and creates an image.

The basic flow is:

Dockerfile
    ↓ docker build
Docker Image
    ↓ docker run
Container
2. Main Dockerfile instructions
FROM — Base image

FROM specifies the base image for your image.

FROM python:3.12-slim

This means:

Start with the Python 3.12 slim image.

Another example:

FROM ubuntu:24.04
Interview point

Almost every Dockerfile starts with FROM.

Interview answer:

"FROM defines the base image from which the new image is built."

3. RUN — Execute commands while building

RUN executes a command during image build time.

RUN apt-get update && apt-get install -y curl

Or:

RUN pip install -r requirements.txt

The result of the command becomes part of an image layer.

Important distinction
RUN npm install

happens during:

docker build

not when the container starts.

Interview trap 🚨

Don't confuse:

RUN      → build time
CMD      → container runtime
ENTRYPOINT → container runtime
4. COPY — Copy files into image

COPY copies files from the build context into the image.

COPY app.py /app/

Or:

COPY . .

Meaning:

Copy the application files from the current build context into the current working directory inside the image.

Best practice

Instead of immediately doing:

COPY . .
RUN pip install -r requirements.txt

you can often do:

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

Why?

Because Docker can reuse the dependency-install layer if requirements.txt hasn't changed, improving build-cache efficiency.

5. CMD — Default command

CMD specifies the default command/arguments to run when a container starts.

Example:

CMD ["python", "app.py"]

When you run:

docker run myapp

Docker runs:

python app.py

But CMD can be overridden:

docker run myapp python test.py
Interview point

"CMD provides the default command for the container and can be overridden at runtime."

6. ENTRYPOINT — Main executable

ENTRYPOINT defines the main executable for the container.

Example:

ENTRYPOINT ["python"]

Then:

CMD ["app.py"]

Together:

ENTRYPOINT ["python"]
CMD ["app.py"]

results in:

python app.py

If you run:

docker run myapp test.py

the arguments supplied at runtime are typically passed to the entrypoint:

python test.py
CMD vs ENTRYPOINT

This is very commonly asked in interviews.

| CMD                                | ENTRYPOINT                                           |
| ---------------------------------- | ---------------------------------------------------- |
| Provides default command/arguments | Defines the main executable                          |
| Easier to override                 | Designed to be harder to replace accidentally        |
| Often used for defaults            | Often used when container behaves like an executable |

Easy way to remember

ENTRYPOINT = what the container is
CMD = default arguments/command

A common pattern is:

ENTRYPOINT ["python"]
CMD ["app.py"]
7. ENV — Environment variables

ENV sets environment variables inside the image/container.

ENV APP_ENV=production
ENV PORT=8000

Your application can access them.

For example:

APP_ENV=production
PORT=8000
DevOps importance

Environment variables are commonly used to configure applications without changing the image.

For example:

Same image
    │
    ├── Dev → APP_ENV=dev
    ├── QA  → APP_ENV=qa
    └── Prod → APP_ENV=prod
Security interview point 🚨

Don't put passwords, API keys, or secrets directly in a Dockerfile using ENV.

For example, avoid:

ENV DB_PASSWORD=mysecret

Use a proper secrets mechanism instead.

8. EXPOSE — Document intended port

EXPOSE tells Docker/users which port the application intends to listen on.

EXPOSE 8000

Important:

EXPOSE does not actually publish the port to the host.

For example:

EXPOSE 8000

doesn't mean you can automatically access it from the host.

You can publish a port with:

docker run -p 8000:8000 myapp

Meaning:

Host port 8000
       ↓
Container port 8000
Interview trap 🚨

EXPOSE ≠ publish port

9. WORKDIR — Set working directory

WORKDIR sets the working directory for subsequent Dockerfile instructions and the container's default working directory.

WORKDIR /app

Then:

COPY . .

means:

Copy files → /app

You don't need:

RUN cd /app

because WORKDIR handles it.

10. Complete example

Let's put everything together:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_ENV=production

EXPOSE 8000

ENTRYPOINT ["python"]

CMD ["app.py"]
What happens?

Step 1

FROM python:3.12-slim

Start from Python base image.

Step 2

WORKDIR /app

Set /app as the working directory.

Step 3

COPY requirements.txt .

Copy dependency file into /app.

Step 4

RUN pip install ...

Install dependencies during image build.

Step 5

COPY . .

Copy application source code.

Step 6

ENV APP_ENV=production

Set environment configuration.

Step 7

EXPOSE 8000

Document that the application is expected to use port 8000.

Step 8

ENTRYPOINT ["python"]
CMD ["app.py"]

When the container starts:

python app.py
11. Most important interview comparison

Memorize this table:

| Instruction  | Purpose                   | When?                 |
| ------------ | ------------------------- | --------------------- |
| `FROM`       | Select base image         | Build                 |
| `RUN`        | Execute command           | Build                 |
| `COPY`       | Copy files into image     | Build                 |
| `WORKDIR`    | Set working directory     | Build/runtime context |
| `ENV`        | Set environment variable  | Build/runtime         |
| `EXPOSE`     | Document intended port    | Metadata              |
| `CMD`        | Default command/arguments | Runtime               |
| `ENTRYPOINT` | Main executable           | Runtime               |

⭐ Interview-ready answer

If the interviewer asks:

"What is a Dockerfile and explain its main instructions?"

You can answer:

"A Dockerfile is a text file containing instructions used to build a Docker image. FROM specifies the base image, RUN executes commands during image build, and COPY copies application files into the image. WORKDIR sets the working directory, while ENV defines environment variables. EXPOSE documents the port the application is expected to listen on. CMD defines the default command or arguments when the container starts, while ENTRYPOINT defines the main executable.

For example, I might use FROM to select a Python base image, WORKDIR to set /app, COPY to add the application, RUN to install dependencies, EXPOSE for the application port, and CMD or ENTRYPOINT to start the application."

🧠 Super-short memory trick
FROM       → Base
RUN        → Build
COPY       → Files
WORKDIR    → Location
ENV        → Configuration
EXPOSE     → Port documentation
ENTRYPOINT → Main executable
CMD        → Default arguments/command

One especially important DevOps interview distinction:

RUN                    → happens while BUILDING the image
CMD / ENTRYPOINT       → happens when RUNNING the container

That distinction is asked very frequently.