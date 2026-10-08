```
•How do containers work internally? (namespaces, cgroups, union file system)

Absolutely. For a DevOps interview, this is a very common follow-up after “What is a container?” The interviewer wants to know whether you understand that containers are not mini-VMs—they are built using Linux kernel features.

How containers work internally

At a high level:

                 Container
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
   Namespaces      cgroups    Union File System
   "Isolation"   "Resources"    "Filesystem"
        │            │            │
        └────────────┼────────────┘
                     ↓
                Linux Kernel
                     ↓
                Host Machine

The three concepts to remember are:

Namespaces = What the container can see
cgroups = What the container can use
Union filesystem = What the container's filesystem looks like

1. Namespaces — Isolation

Namespaces isolate processes so that a container gets its own view of certain system resources.

For example, a process running inside a container shouldn't normally see all the processes running on the host.

Linux provides several namespaces:

| Namespace  | What it isolates                 |
| ---------- | -------------------------------- |
| **PID**    | Process IDs                      |
| **NET**    | Network interfaces, IPs, routing |
| **MNT**    | Mount points/filesystems         |
| **UTS**    | Hostname                         |
| **IPC**    | Inter-process communication      |
| **USER**   | User/group IDs                   |
| **CGROUP** | Cgroup information               |

Example

On the host:

Host
PID 1    systemd
PID 100  nginx
PID 200  sshd
PID 500  docker

Inside a container, because of the PID namespace, the container may see:

Container
PID 1    nginx
PID 2    worker

The container thinks its nginx process is PID 1, even though it has a different PID from the host's perspective.

Interview line

"Namespaces provide isolation by giving containers their own view of processes, networking, mounts, hostnames, users, and other system resources."

2. cgroups — Resource Control

cgroups (Control Groups) control and limit how much of the host's resources a container can consume.

For example, suppose you have:

Server
├── 8 CPU cores
└── 16 GB RAM

You can configure a container with something like:

Container A
CPU: 2 cores
Memory: 2 GB

If the application inside the container tries to consume excessive resources, the cgroup mechanisms can constrain it.

cgroups can manage resources such as:

CPU
Memory
Disk I/O
Network-related accounting/control
Number of processes
Why is this important?

Imagine you have:

Container A → memory-hungry application
Container B → payment service
Container C → monitoring

Without resource controls, Container A could consume most of the host's memory and negatively affect the other workloads.

With cgroups, you can establish resource limits/reservations.

Interview line

"cgroups provide resource management. They allow us to limit and account for CPU, memory, I/O, and other resources consumed by containers."

3. Union File System — Container Filesystem

This is where Docker's image layers come into the picture.

Instead of storing every container as one giant independent filesystem, container images are typically constructed from multiple read-only layers.

For example:

Application layer
       ↓
Python dependencies
       ↓
Python runtime
       ↓
Ubuntu base

Conceptually:

┌─────────────────────────┐
│ Application             │  ← Read-only
├─────────────────────────┤
│ Python dependencies     │  ← Read-only
├─────────────────────────┤
│ Python                  │  ← Read-only
├─────────────────────────┤
│ Ubuntu base             │  ← Read-only
└─────────────────────────┘

When you start a container, a writable layer is placed on top:

┌─────────────────────────┐
│ Writable container layer│
├─────────────────────────┤
│ Application layer       │
├─────────────────────────┤
│ Dependencies layer      │
├─────────────────────────┤
│ Runtime layer           │
├─────────────────────────┤
│ Base image layer        │
└─────────────────────────┘

This is commonly described using UnionFS/overlay-style layered filesystems. Docker on Linux commonly uses OverlayFS through its storage driver.

4. Why are image layers useful?

Suppose you have:

ubuntu
  ↓
python
  ↓
dependencies
  ↓
my-app

If you create another application using the same Ubuntu and Python layers, those existing layers can be reused rather than duplicated.

This saves:

Disk space
Download time
Build time

It also explains why Docker builds can be very fast when previous layers are cached.

5. Put everything together

Suppose you run:

docker run -d --name nginx nginx

Conceptually, the container runtime does something like:

docker run
    │
    ↓
Container Runtime
    │
    ├── Create namespaces
    │       ├── PID
    │       ├── Network
    │       ├── Mount
    │       └── etc.
    │
    ├── Configure cgroups
    │       ├── CPU
    │       ├── Memory
    │       └── I/O
    │
    ├── Mount container image layers
    │       └── Overlay/union filesystem
    │
    └── Start container process

Under the hood, Docker uses a container runtime such as containerd/runc, which interacts with Linux kernel features to create and run the container.

6. A very important interview distinction

An interviewer may ask:

"Does Docker itself create the isolation?"

A good answer:

"Docker provides the container management experience, but the actual isolation and resource control are largely provided by Linux kernel features such as namespaces and cgroups, while the container runtime creates and manages the container processes and filesystem."

This is a stronger answer than simply saying "Docker creates a container."

7. Easy way to remember

Think of a container as an apartment:

Namespaces = walls 👈

Each tenant sees their own apartment and doesn't normally see the other tenant's rooms.

cgroups = utility limits

The landlord can say:

"Your apartment gets this much electricity/water."

Similarly, cgroups control resource consumption.

Union filesystem = apartment contents

The building provides common/base components, while each apartment gets its own writable space.

So:

NAMESPACES
    ↓
Isolation / Visibility

CGROUPS
    ↓
Resource limits

UNION/OVERLAY FILESYSTEM
    ↓
Layered container filesystem
⭐ Best interview answer

If the interviewer asks "How do containers work internally?", give this:

"Containers are implemented using operating-system-level virtualization rather than running a complete guest OS like a VM. On Linux, namespaces provide isolation by giving each container its own view of processes, networking, mounts, hostnames, and users. cgroups control and account for resources such as CPU and memory so that one container cannot freely consume all the host resources.

For the filesystem, container images are typically made up of multiple read-only layers, and a writable layer is added when a container runs. Technologies such as OverlayFS provide this layered filesystem behavior.

A container runtime, such as runc, uses these Linux kernel features to create and run the isolated process. Docker provides the higher-level tooling for building, distributing, and managing these containers."

🎯 10-second version

If they want a short answer:

"Containers work mainly through three Linux concepts: namespaces for isolation, cgroups for resource control, and layered filesystems such as OverlayFS for efficient image storage. Unlike VMs, containers share the host's kernel."

Interview sequence to memorize:

Container → Namespaces → cgroups → Image layers → Runtime → Docker/Kubernetes.