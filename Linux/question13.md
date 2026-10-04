```

•What is swap? When is it used?


For a DevOps interview, the simplest way to understand swap is:

Swap is disk space that Linux can use as an extension of RAM when the system is under memory pressure.

1. RAM vs Swap

Think of it like this:

RAM
 ↓
Fast memory used by running applications

        ↓ RAM becomes pressured

SWAP
 ↓
Disk space used for less-active memory pages

Swap is much slower than RAM, so it is not a replacement for having enough RAM.

2. When is swap used?

Suppose your server has:

RAM = 8 GB

and applications are consuming almost all of it.

Linux may move some less-active memory pages from RAM to swap:

RAM
┌─────────────────────┐
│ Active pages        │
│ Active pages        │
│ Less-active pages ──┼──────→ SWAP
└─────────────────────┘

This frees RAM for processes that currently need it.

3. How do you check swap?
free -h
free -h

Example:

               total    used    free
Mem:             16Gi    14Gi    2Gi
Swap:             4Gi     1Gi    3Gi

This tells you:

RAM  = 16 GB total
RAM  = 14 GB used

Swap = 4 GB total
Swap = 1 GB used
swapon --show
swapon --show

This shows configured swap devices/files.

4. How do you know whether the server is actively swapping?

Use:

vmstat 2

Pay attention to:

si    so

Where:

si → swap in
so → swap out

For example:

procs -----------memory---------- ---swap--
 r  b   swpd   free   ...         si   so
 2  0   1024   2000              0    0
 3  1   2048   1000            500  2000
 4  2   2500    500           1000  3000

If si/so are continuously high, that's a sign you should investigate memory pressure.

5. Is using swap always bad?

No.

This is an important interview point.

Seeing:

Swap: 4G total
Swap: 500M used

doesn't automatically mean there's a problem.

The more important question is:

Is the system actively swapping and experiencing performance problems?

Heavy swapping can cause:

Memory pressure
      ↓
Pages moved between RAM ↔ disk
      ↓
More disk I/O
      ↓
Higher latency
      ↓
Application becomes slow

If the system spends excessive time moving pages instead of doing useful work, this can lead to thrashing.

6. DevOps troubleshooting scenario

Imagine users say:

"Our application has suddenly become very slow."

You run:

free -h

and see very high RAM usage.

Then:

vmstat 2

shows sustained swap activity.

You would investigate which processes are consuming memory:

top

or:

htop

You might find:

java     → 6 GB
python   → 2 GB

Then you'd investigate whether:

the application has a memory leak
workload increased
memory limits are incorrect
the server needs more RAM
a process is consuming unexpectedly large amounts of memory

Don't immediately solve it by simply increasing swap. That may prevent an immediate out-of-memory failure in some situations, but it doesn't fix an underlying memory problem and can make a heavily swapping system very slow.

⭐ Interview answer

If the interviewer asks:

"What is swap? When is it used?"

You can say:

"Swap is disk space that Linux uses as additional virtual memory when there is memory pressure. The kernel can move less-active memory pages from RAM to swap to free RAM for active processes. Because disk is much slower than RAM, heavy swapping can significantly impact performance. I would check free -h for memory and swap usage and use vmstat to check si and so for active swapping."

🧠 Remember this
RAM  → fast
Swap → slow

RAM under pressure
       ↓
Swap may be used
       ↓
Heavy continuous swapping
       ↓
Performance problem

Most useful commands for the interview:

free -h
swapon --show
vmstat 2
top

And the key distinction:

Swap usage ≠ automatically a problem. Heavy/continuous swapping + performance degradation = investigate memory pressure.