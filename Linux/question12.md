```

•top vs htop vs vmstat vs iostat


For a DevOps interview, think of these tools as answering different troubleshooting questions:

top = What is happening right now?
htop = Same idea, but more interactive/user-friendly.
vmstat = Is the system under CPU, memory, or I/O pressure?
iostat = Is disk/storage I/O the bottleneck?

1. top — overall real-time system view

Run:

top

You'll get something like:

%Cpu(s): 75.0 us, 10.0 sy,  0.0 ni, 10.0 id, 5.0 wa
MiB Mem : 16000 total, 2000 free, 10000 used

And below that, processes:

PID    USER     %CPU   %MEM   COMMAND
1234   app      85.0    5.2   java
2345   root     20.0    2.1   nginx
What can you investigate?
CPU usage
Memory usage
Load average
Running processes
Which process consumes the most CPU
Which process consumes the most memory
Process IDs
Process states

Useful keys inside top:

P → sort by CPU
M → sort by memory
k → send signal to a process
q → quit
DevOps scenario

Application is slow:

top

You discover:

java    90% CPU

Now you have a lead: investigate the Java process.

2. htop — interactive alternative to top

Run:

htop

It provides a more interactive interface.

You'll typically see CPU/core usage, memory, load average, and processes in a more visual layout.

You can:

scroll through processes
sort processes
search
interact with processes
send signals
inspect resource usage

For example, you might identify:

PID     CPU%     MEM%     COMMAND
1234    95       10       java
top vs htop
| `top`                         | `htop`                      |
| ----------------------------- | --------------------------- |
| Usually available by default  | May need installation       |
| Text-based                    | More interactive            |
| Excellent for servers         | Easier to navigate          |
| Lightweight                   | More user-friendly          |
| Standard troubleshooting tool | Convenient interactive tool |


Interview tip: Don't say "htop is more powerful" as your main distinction. The important point is that both monitor processes/system resources; htop provides a more interactive interface.

3. vmstat — CPU + memory + processes + I/O

This one is especially useful when you want to understand system-wide resource pressure rather than just looking at individual processes.

Run:

vmstat

Or for continuous monitoring:

vmstat 2

This reports every 2 seconds.

You may see:

procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs  us sy id wa
 2  0      0  2048  1000   5000    0    0   100   200 1000 2000  60 10 25  5

The exact columns can look intimidating, but for interviews focus on these:

r

Runnable processes.

r = 8

means there are many processes ready to run.

Compare this with your CPU count.

b

Processes blocked, commonly waiting for I/O.

b = 5

can be a clue that processes are blocked.

si / so

Swap in / swap out.

si → swap data coming into RAM
so → swap data going out of RAM

Sustained swapping can indicate memory pressure.

bi / bo

Block I/O:

bi → blocks received from a device
bo → blocks sent to a device
us

CPU time spent in user processes.

sy

CPU time spent in the kernel/system.

id

CPU idle time.

wa

CPU time waiting for I/O.

4. iostat — investigate disk/storage I/O

Run:

iostat

For extended statistics:

iostat -xz 2

This is particularly useful when you suspect disk/storage is causing application slowness.

You might see:

Device   r/s   w/s   rkB/s   wkB/s   %util
sda      100   200   5000    10000   95.0

Important metrics vary somewhat by iostat version and options, but commonly you'll look at:

read/write operations
throughput
latency/await
device utilization
I/O queue-related metrics

For example, high I/O activity and latency can point you toward a storage bottleneck.

5. How they fit together in a real incident

Imagine:

"Production application is very slow."

Don't randomly restart things. Start investigating.

Step 1 — Overall picture
top

Ask:

Is CPU very high?
Is memory exhausted?
Is load average high?
Which process is consuming resources?
Step 2 — More interactive process investigation
htop

Find the problematic process and inspect it.

Step 3 — System-level resource pressure
vmstat 2

Look for clues such as:

high r → CPU/run-queue pressure
high b → blocked processes
high si/so → swapping
high wa → I/O wait
Step 4 — If I/O looks suspicious
iostat -xz 2

Now investigate the disks/devices.

You might discover:

High disk latency
High device utilization

That gives you evidence that storage I/O needs investigation.

⭐ The interview comparison
| Tool     | Main purpose                            | Think                             |
| -------- | --------------------------------------- | --------------------------------- |
| `top`    | Processes + overall resources           | **What's happening now?**         |
| `htop`   | Interactive process/resource monitoring | **Easier way to investigate**     |
| `vmstat` | CPU, memory, processes, swap, I/O       | **Is the system under pressure?** |
| `iostat` | Storage/device I/O                      | **Is disk I/O the bottleneck?**   |

🧠 Easy memory trick
top
 ↓
Overall + processes

htop
 ↓
Interactive top

vmstat
 ↓
CPU + Memory + VM + I/O

iostat
 ↓
I/O / Disks
⭐ Strong DevOps interview answer

If asked:

"What's the difference between top, htop, vmstat and iostat?"

Say:

"top gives me a real-time overview of system resources and processes, while htop provides a more interactive interface for similar process monitoring. vmstat gives system-wide statistics about CPU, memory, processes, swapping and I/O, which helps identify resource pressure. iostat focuses more specifically on CPU and storage-device I/O, so I'd use it when I suspect disk or storage performance is causing the problem."

A good troubleshooting sequence to remember is:

Application slow
      ↓
    top/htop
      ↓
CPU? Memory? Load?
      ↓
    vmstat
      ↓
CPU / memory / swap / I/O pressure?
      ↓
    iostat
      ↓
Is storage I/O the problem?

That "which tool would you use and why?" reasoning is often more valuable in a DevOps interview than simply memorizing the commands.