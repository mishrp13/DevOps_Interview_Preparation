```

8.  Process vs thread. What are zombie and orphan processes?



Process vs Thread — Interview Perspective

The easiest way to remember:

Process = independent running program
Thread = execution unit inside a process

1. What is a Process?

A process is a program that is currently executing.

For example, when you run:

./app

Linux creates a process for that program.

A process has its own:

PID (Process ID)
Virtual address space
Code
Data
Heap
Stack
Open file descriptors
Security credentials
Other process resources

You can see processes with:

ps aux

or:

top

Example:

PID    COMMAND
1200   nginx
1300   sshd
1400   python
2. What is a Thread?

A thread is an execution path within a process.

A process can contain multiple threads.

For example:

Process: Web Server
        │
        ├── Thread 1
        ├── Thread 2
        ├── Thread 3
        └── Thread 4

Threads within the same process share:

Code
Data
Heap
Open files
Address space

But each thread has its own:

Stack
Registers
Program counter
Thread ID
3. Process vs Thread

| Feature       | Process                               | Thread                               |
| ------------- | ------------------------------------- | ------------------------------------ |
| Independence  | More independent                      | Part of a process                    |
| Address space | Own                                   | Shares process address space         |
| Memory        | Separate                              | Shared with other threads            |
| Communication | More expensive                        | Easier/faster                        |
| Creation      | Relatively expensive                  | Cheaper                              |
| Failure       | Usually isolated from other processes | Bad thread can affect entire process |
| ID            | PID                                   | TID                                  |
| Example       | Browser process                       | Browser worker thread                |

Interview answer

A process has its own virtual address space and resources, while threads are execution units within a process that share the process's address space and resources.

4. Why use threads?

Suppose a web server needs to handle 1,000 requests.

A multithreaded application can have:

Web Server Process
       │
       ├── Thread → Request 1
       ├── Thread → Request 2
       ├── Thread → Request 3
       └── Thread → Request 4

Because threads share memory, communication between them can be faster than communication between separate processes.

But shared memory also creates synchronization problems such as:

Race conditions
Deadlocks
Data corruption

5. What is a Zombie Process? ⭐

A zombie process is a child process that has finished execution, but its parent hasn't yet collected its exit status.

Think:

Child
  │
  │ exits
  ▼
Zombie
  │
  │ waiting for parent to collect exit status
  ▼
Parent calls wait()
  │
  ▼
Zombie removed

The process has already finished executing.

It is not actually running.

But its entry remains in the process table so the parent can retrieve information such as its exit status.

Example

Suppose:

Parent PID = 1000
Child PID  = 1001

Child finishes:

1001 → EXITED

But parent doesn't call:

wait()

The child becomes:

1001 → ZOMBIE

You might see:

Z

in the process state.

For example:

ps aux

may show:

user   1001   ...   Z   child <defunct>

<defunct> is commonly seen for zombie processes.

6. How do you identify zombies?
ps aux | grep ' Z '

or:

ps -eo pid,ppid,state,cmd

Look for:

STATE = Z

You can also look for:

<defunct>
7. How do you handle a zombie?

This is a common interview trick.

You cannot normally kill a zombie with kill -9, because the process has already exited.

The important question is:

Why hasn't the parent collected the child's exit status?

The parent should call:

wait()

or:

waitpid()

If the parent is stuck or badly designed, you may need to investigate or restart the parent process.

Interview answer

A zombie has already terminated. Its parent hasn't collected its exit status using wait()/waitpid(). Killing the zombie itself doesn't solve the problem; the parent needs to reap it.

8. What is an Orphan Process? ⭐

An orphan process is a running child process whose parent process has terminated.

Example:

Parent
  │
  └── Child
        │
        │ parent exits
        ▼
     Orphan

The child is still running, but its original parent is gone.

Linux then re-parents the orphan to another process, traditionally PID 1 (init/systemd) or an appropriate subreaper where applicable.

Conceptually:

Before:

PID 1000
  │
  └── PID 1001


Parent 1000 exits:

PID 1001
  │
  └── re-parented
        ↓
      PID 1
9. Zombie vs Orphan

This is very frequently asked.

|                   | Zombie                         | Orphan                                |
| ----------------- | ------------------------------ | ------------------------------------- |
| Child running?    | ❌ No                           | ✅ Usually yes                         |
| Parent alive?     | Usually yes                    | ❌ No                                  |
| Main issue        | Exit status not collected      | Original parent terminated            |
| Re-parented?      | Not in the normal orphan sense | ✅ Yes                                 |
| `kill -9` useful? | ❌ No, already exited           | Can terminate it if appropriate       |
| State             | `Z`                            | Usually normal running/sleeping state |

Easy memory trick

Zombie = child is dead, parent is alive but hasn't cleaned it up.

Orphan = child is alive, parent is dead.

⭐ Classic interview scenario
Interviewer:

What happens if a parent process terminates before its child?

Answer:

The child becomes an orphan. Linux re-parents it to PID 1 or another designated subreaper, which can then take responsibility for reaping it when it eventually exits.

Interviewer:

What happens if the child terminates before the parent?

Answer:

The child can temporarily become a zombie until the parent calls wait() or waitpid() to collect its exit status.

🧠 One diagram to remember
             Parent
            /      \
           /        \
      Child A      Child B
         │             │
      exits          parent exits
         │             │
         ▼             ▼
      ZOMBIE         ORPHAN
         │             │
     wait()         re-parent
         │             │
         ▼             ▼
      removed       continues
⭐ 30-second interview answer

A process is an independent execution environment with its own virtual address space, while a thread is an execution unit inside a process and shares its memory and resources. A zombie is a child that has terminated but whose parent hasn't collected its exit status. An orphan is a child that is still running after its parent has terminated, so it gets re-parented, typically to PID 1 or an appropriate subreaper.

Useful Linux commands
ps aux
ps -ef
top
pstree -p
ps -eo pid,ppid,state,cmd

The particularly useful columns to remember are:

PID  → Process ID
PPID → Parent Process ID
STAT → Process state

For troubleshooting, PID + PPID + STAT often tells you a lot about what's happening.


--------------------------------------------------------------------------------------------------------------

