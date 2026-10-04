```
•What are cgroups and namespaces? (The foundation of containers, so this links to Docker)

For a DevOps interview, this is one of the most important Linux concepts behind Docker and containers.

The easiest way to remember it is:

Namespaces = isolation
cgroups = resource control

Together, they are a major part of how Linux containers work.

1. What are Linux namespaces?

A namespace isolates what a process can see.

Imagine two containers running on the same Linux host:

Host
│
├── Container A
│    └── nginx
│
└── Container B
     └── nginx

Both containers may have processes, network interfaces, PIDs, hostnames, etc.

Namespaces make each container see an isolated view of the system.

For example, a process inside a container can have a PID that looks like:

PID 1

while on the host the same process might have:

PID 24567

The container sees its own process namespace.

2. What do namespaces isolate?

Linux has several namespace types.

For a DevOps interview, know these:

| Namespace   | What it isolates                  |
| ----------- | --------------------------------- |
| **PID**     | Process IDs                       |
| **Network** | Network interfaces, routes, ports |
| **Mount**   | Filesystem mount points           |
| **UTS**     | Hostname/domain name              |
| **IPC**     | Inter-process communication       |
| **User**    | User/group IDs                    |
| **Cgroup**  | Cgroup hierarchy view             |


You don't necessarily need to memorize every detail, but PID + Network + Mount + User are particularly useful to understand.

3. PID namespace example

Suppose the host has:

Host:
PID 1
PID 100
PID 200
PID 300
PID 24567

A container may see:

Container:
PID 1
PID 2
PID 3

The container doesn't see the host's complete process tree in the same way.

That's PID namespace isolation.

This is one reason you can have:

docker exec <container> ps

and see a much smaller process list than you see on the host.

4. Network namespace

A container can have its own:

network interface
IP address
routing table
network namespace

Conceptually:

Host network namespace
        │
        ├── eth0
        │
        └── ...

Container network namespace
        │
        ├── eth0
        ├── IP address
        └── routes

This helps containers have isolated networking.

Docker then builds networking on top of these Linux capabilities.

For example:

docker run -p 8080:80 nginx

Docker configures networking so traffic arriving at host port 8080 can reach port 80 in the container.

5. Mount namespace

Mount namespaces provide filesystem/mount isolation.

A container can have its own view of the filesystem.

For example:

Container
/
├── bin
├── etc
├── app
└── var

This doesn't mean the container magically has a completely separate physical disk.

Rather, Linux provides the process with an isolated mount view, typically combined with container filesystems and other mechanisms.

6. Now: What are cgroups?

cgroups = control groups.

They control and account for resource usage by groups of processes.

Think:

Namespaces → "What can you see?"

cgroups    → "How many resources can you use?"

For example, you might want a container to have:

CPU    → limited
Memory → 512 MB
PIDs   → maximum 100

cgroups can enforce resource limits/accounting for these resources.

7. Docker example

Suppose you run:

docker run --memory=512m --cpus=1 nginx

You're telling Docker that this container should have resource constraints roughly corresponding to:

Memory → 512 MB
CPU    → 1 CPU worth of quota

Docker uses Linux kernel mechanisms, including cgroups, to enforce resource controls.

So:

docker run
    ↓
Docker/container runtime
    ↓
Linux kernel
    ├── namespaces → isolation
    └── cgroups    → resource control
8. Why are cgroups important in DevOps?

Imagine you have:

Server: 8 CPU / 16 GB RAM

Container A → application
Container B → database
Container C → monitoring

Without appropriate resource controls, one workload could potentially consume a disproportionate amount of the host's resources.

You can use resource limits to constrain workloads.

For example:

docker run \
  --memory=1g \
  --cpus=2 \
  my-app

Conceptually:

Container
 ├── CPU limit → 2 CPUs
 └── Memory limit → 1 GB

This is particularly important in shared environments.

9. What happens if a container exceeds its memory limit?

This is a great interview follow-up.

Suppose:

docker run --memory=512m my-app

and the workload tries to consume significantly more memory.

The cgroup memory limit can prevent it from simply consuming unlimited host memory.

Depending on the circumstances, the kernel may reclaim memory and, if the container remains over its limit and memory cannot be reclaimed, processes can be killed due to an out-of-memory condition.

This is why you might see a container suddenly exit or be killed when it has an inappropriate memory limit.

10. Namespaces + cgroups together

This is the key interview diagram:

                 Linux Host
                     │
              Linux Kernel
                     │
          ┌──────────┴──────────┐
          │                     │
     Namespaces              cgroups
          │                     │
     "Isolation"          "Resource control"
          │                     │
    ┌─────┴─────┐        ┌──────┴──────┐
    │           │        │             │
 Container A  Container B  CPU        Memory
    │           │
    └─────┬─────┘
          │
       Processes

Or remember:

Container
   │
   ├── Namespace → isolated view
   │
   └── cgroup    → resource limits/accounting
11. Are containers virtual machines?

This is another common follow-up.

Containers are not the same as traditional VMs.

A VM typically has:

Physical machine
      ↓
Hypervisor
      ↓
Virtual machine
      ↓
Guest OS
      ↓
Application

Containers typically look more like:

Physical/VM host
      ↓
Linux kernel
      ↓
Container runtime
      ↓
Namespaces + cgroups
      ↓
Container processes

Containers generally share the host kernel, whereas a VM has its own guest kernel.

That's a fundamental difference.

⭐ Interview answer

If the interviewer asks:

"What are cgroups and namespaces?"

A strong answer is:

"Namespaces and cgroups are fundamental Linux kernel mechanisms used by container runtimes. Namespaces provide isolation by giving processes an isolated view of things like processes, networking, mounts and users. Cgroups, or control groups, provide resource control and accounting, such as limiting CPU and memory usage. Docker uses these Linux mechanisms, together with other components such as filesystem isolation, to implement containers."

Then give the interviewer this simple example:

docker run --memory=512m --cpus=1 nginx

Explain:

Namespaces
    ↓
Container gets isolated environment

cgroups
    ↓
Container gets CPU/memory constraints
🧠 Best memory trick

Namespace = "What can I see?"
cgroup = "How much can I use?"

And if they ask:

"Are namespaces enough to create a container?"

Don't say simply "yes."

A better answer is:

"Namespaces and cgroups are foundational mechanisms, but a production container also involves other pieces such as filesystem/root filesystem setup, capabilities, security mechanisms, networking, and a container runtime."

That answer shows you understand that Docker is more than just namespaces + cgroups.