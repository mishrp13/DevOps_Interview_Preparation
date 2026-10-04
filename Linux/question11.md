```
•What does load average mean? What do the 3 numbers represent?

For a DevOps interview, load average is a very common Linux troubleshooting topic.

When you run:

uptime

you might see:

10:30:15 up 20 days,  3:12,  2 users,  load average: 1.20, 0.80, 0.50

The three numbers are:

1.20    0.80    0.50
 │        │       │
 │        │       └── 15-minute average
 │        └────────── 5-minute average
 └────────────────── 1-minute average

So:

The three numbers represent the average system load over the last 1, 5, and 15 minutes.

What does "load" actually mean?

This is the part interviewers care about.

Linux load average represents the average number of tasks that are:

running or ready to run on the CPU, and
on Linux, tasks in uninterruptible sleep, commonly associated with waiting on I/O.

So it's not simply:

"CPU utilization."

That's an important distinction.

For example:

CPU utilization = 30%
Load average   = 8

is possible if many tasks are blocked waiting for I/O.

CPU cores matter ⭐

Suppose your server has 4 CPU cores.

You might see:

load average: 1.00, 1.00, 1.00

Roughly speaking, a load of 1.00 means about one runnable/load-contributing task on average.

With 4 cores:

Load 1  → relatively light
Load 4  → roughly all cores busy
Load 8  → more work than the CPUs can immediately handle

A useful way to think about it is:

Load average ÷ number of CPU cores

For example:

8 load / 4 CPUs = 2.0

That indicates the system has substantially more load than its CPU capacity at that moment/period.

But don't interpret the number as a direct percentage. Load average and CPU utilization are different metrics.

DevOps troubleshooting example

Imagine you have:

uptime

and get:

load average: 12.0, 10.0, 8.0

Your machine has:

nproc

Output:

4

So you have 4 CPUs.

The load has been high for a sustained period:

1 min  → 12
5 min  → 10
15 min → 8

This tells you the system has had significant load, and it's increasing toward the present.

At this point, don't immediately conclude "CPU is the problem."

Investigate.

For example:

top

or:

htop

Check:

CPU usage
memory usage
processes consuming CPU
I/O wait
system load
process states

You can also check CPU information:

nproc

and:

lscpu
Very important interview distinction

Suppose:

load average: 8, 8, 8

on an 8-core machine.

That doesn't automatically mean:

"The server is overloaded."

It could mean the system has roughly enough runnable load to keep the 8 CPUs busy.

But:

load average: 8, 8, 8

on a 2-core machine indicates a very different situation.

That's why you should always consider CPU count + load average + CPU/I/O metrics together.

What do the three numbers tell you?

Suppose:

load average: 2.0, 5.0, 8.0

Reading left to right:

1 min  = 2
5 min  = 5
15 min = 8

The recent load is lower than the previous 15 minutes.

So the load appears to be coming down.

Now:

load average: 8.0, 5.0, 2.0

means:

1 min  = 8
5 min  = 5
15 min = 2

The recent load is higher than the longer-term average, so the load appears to be increasing.

This is useful during incident troubleshooting.

DevOps scenario

Imagine users report:

"The application has suddenly become slow."

You run:

uptime
load average: 10.5, 8.2, 3.1

Then:

nproc
4

The load has increased significantly in the recent period.

Now investigate with:

top

You might discover:

Scenario A — CPU problem
CPU usage → 100%

A process may be consuming CPU.

Scenario B — I/O problem

CPU isn't fully utilized, but many processes are waiting on I/O.

You might investigate with:

iostat

or:

vmstat

So load average tells you that there is system pressure/work, but you need additional tools to determine why.

⭐ Interview answer

If the interviewer asks:

"What does load average mean? What do the three numbers represent?"

A strong answer is:

"Load average represents the average number of tasks that are runnable or waiting in certain uninterruptible states. The three numbers represent the average load over the last 1 minute, 5 minutes, and 15 minutes. I also compare the load with the number of CPU cores. A load of 4 means something very different on a 4-core machine versus a 16-core machine. I would use tools like top, vmstat, or iostat to determine whether the load is caused by CPU pressure, I/O, or another issue."

🧠 Easy memory trick
load average:  1m    5m    15m
               ↓     ↓      ↓
              2.0   1.5    1.0

And remember:

Load average ≠ CPU utilization.