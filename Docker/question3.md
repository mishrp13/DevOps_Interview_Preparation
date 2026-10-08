```
•Image vs container vs registry

For a DevOps interview, think of these three as a simple flow:

Image → Container → Registry

        BUILD
          ↓
     Docker Image
          ↓
       RUN
          ↓
     Container
          ↑
          │ pull / push
          ↓
       Registry
1. What is an Image?

A container image is an immutable package containing everything needed to create and run a container:

Application code
Runtime
Libraries/dependencies
System tools
Configuration/defaults
Filesystem layers

Example:

docker build -t myapp:1.0 .

This creates an image:

myapp:1.0

Think of an image as a blueprint/template.

Important interview point

An image is not running.

Image = blueprint
Container = running instance of that blueprint

An image is generally built in layers and is treated as immutable; when a container runs, it gets a writable container layer on top.

2. What is a Container?

A container is a running (or created) instance of an image, with its own isolated process environment, networking, filesystem view, etc.

For example:

docker run -d --name myapp myapp:1.0

Conceptually:

Image
myapp:1.0
     │
     │ docker run
     ↓
Container
myapp-container

You can create multiple containers from the same image:

              myapp:1.0
             /    |    \
            ↓     ↓     ↓
        Container Container Container
           A         B        C

Each container can have its own:

Process state
Network configuration
Writable filesystem layer
Environment variables
Resource limits

But they can share the underlying image layers.

Interview line

"An image is a read-only, immutable package, while a container is an isolated runtime instance created from that image."

3. What is a Registry?

A container registry is a service used to store, distribute, and version container images.

Think of it as a repository for container images.

Examples include:

Docker Hub
Amazon ECR
Google Artifact Registry
Azure Container Registry
GitHub Container Registry
Self-hosted registries

For example:

docker push myregistry/myapp:1.0

Later, another server can do:

docker pull myregistry/myapp:1.0

Then:

docker run myregistry/myapp:1.0
4. Complete DevOps workflow

This is particularly important for interviews because it connects the three concepts to CI/CD.

Developer
    │
    ↓
Source Code
    │
    ↓
CI Pipeline
    │
    │ docker build
    ↓
Docker Image
    │
    │ docker push
    ↓
Container Registry
    │
    │ docker pull
    ↓
Deployment Server
    │
    │ docker run
    ↓
Container

For example:

Git → Jenkins/GitHub Actions
          ↓
     Build Image
          ↓
    myapp:1.5
          ↓
      Push to ECR
          ↓
   Kubernetes pulls it
          ↓
       Pod/Container

This is how containers commonly fit into a DevOps pipeline.

5. |                | Image               | Container                  | Registry                           |
| -------------- | ------------------- | -------------------------- | ---------------------------------- |
| What is it?    | Package/template    | Running instance           | Image storage/distribution service |
| Purpose        | Package application | Run application            | Store/share images                 |
| Mutable?       | Generally immutable | Has writable runtime layer | Stores image versions              |
| Example        | `nginx:1.27`        | `my-nginx-container`       | Docker Hub / ECR                   |
| Created by     | `docker build`      | `docker run`               | Registry service                   |
| Main operation | Build               | Run/stop/delete            | Push/pull                          |

6. Very common interview question
Interviewer: "Can I have multiple containers from one image?"

Yes.

              nginx:latest
                  │
       ┌──────────┼──────────┐
       ↓          ↓          ↓
   Container 1 Container 2 Container 3

The containers can share the image's read-only layers while each has its own runtime state and writable layer.

Interviewer: "Can a container exist without an image?"

For the normal Docker/container workflow, a container is created from an image. The container runtime needs a root filesystem/image content to start the container.

Interviewer: "Where does Kubernetes get its images?"

Usually from a container registry.

For example:

Kubernetes
     ↓
containerd / CRI
     ↓
Container Registry
     ↓
myapp:1.5

The node pulls the required image and then creates the container.

⭐ Best interview answer

If the interviewer asks:

"Explain image, container and registry."

Say:

"A container image is an immutable package containing the application and all its required dependencies and filesystem layers. A container is a runtime instance created from that image. Multiple containers can be created from the same image.

A container registry is a centralized location for storing, versioning, and distributing container images. In a typical DevOps pipeline, CI builds the image, pushes it to a registry, and during deployment the target environment pulls that image and runs it as a container.

So, in simple terms: an image is the blueprint, a container is the running instance, and a registry is where we store and distribute the blueprints."

🧠 Remember this
IMAGE     = What to run
CONTAINER = Running it
REGISTRY  = Where the image is stored

And for a DevOps interview, connect it to:

Code → Build Image → Push Registry → Pull Image → Run Container

That single flow will help you answer several follow-up questions about Docker, CI/CD, Kubernetes, and deployments.