```
•What are image layers? How does layer caching work?

1. What are image layers?

A Docker image is built from multiple layers. Many Dockerfile instructions create layers, and these layers are stacked to form the final image.

Example Dockerfile:


FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]

Think of the image as a stack of layers:

Application layer

COPY app.py .

Dependencies layer

RUN pip install -r requirements.txt

Requirements layer

COPY requirements.txt .

Base image

FROM python:3.12

Key points:

Layers contain filesystem changes made while building the image.

Layers can be reused by multiple images.

Image layers are generally read-only; a running container adds a writable layer on top.

2. How does layer caching work?

Docker caches the results of build steps. If an instruction and its relevant inputs have not changed, Docker can reuse the cached result instead of running that step again.

For example:

FROM python:3.12
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
CMD ["python", "app.py"]

Suppose you change only app.py.

Docker can reuse the cached base image, requirements copy, and dependency installation steps, assuming their cache remains valid.

Docker rebuilds the application copy step.

This makes the build faster because dependencies do not need to be installed again.

If requirements.txt changes, the dependency installation step and subsequent steps generally need to be rebuilt.

3. Best practice to improve caching

Less efficient:

COPY . .
RUN pip install -r requirements.txt

Any change to a file copied by COPY . . can invalidate the cache for the installation step.

Better:

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

This keeps the dependency installation cache reusable when only application code changes.

4. Interview answer to memorize

Docker image layers are filesystem changes created during the image build. Docker uses layer caching to reuse previously built steps when their instructions and inputs have not changed, which reduces build time. To improve caching, I copy dependency files first, install dependencies, and then copy application code.

Interview tip: Remember this phrase: “Copy dependencies first, install them, then copy application code.” It is a common practical example of optimizing Docker builds.