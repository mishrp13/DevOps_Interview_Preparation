```

•What is the difference between kill, kill -9 and kill -15?


For a DevOps interview, this is a very common Linux/process-management question. The key is understanding signals.

When you run:

kill <PID>

you're not necessarily "killing" a process immediately. You're sending a signal to that process.

1. kill PID
kill 1234

By default, kill sends:

SIGTERM (15)

So:

kill 1234

is essentially:

kill -15 1234

SIGTERM means:

"Please terminate gracefully."

The application gets an opportunity to:

finish current work
close files
close database connections
flush logs
release resources
perform cleanup

For example:

kill 1234

The application might handle the signal:

SIGTERM
   ↓
Application receives signal
   ↓
Cleanup
   ↓
Close connections
   ↓
Exit
2. kill -15 PID
kill -15 1234

This explicitly sends SIGTERM (signal 15).

It is the same as:

kill 1234

because SIGTERM is the default signal for kill.

Why is SIGTERM important in DevOps?

Suppose you have a web application running:

Nginx → Application → Database

If you terminate the application gracefully, it can potentially:

Stop accepting new work
        ↓
Finish existing requests
        ↓
Close DB connections
        ↓
Flush logs
        ↓
Exit

This is particularly important during deployments and service restarts.

3. kill -9 PID
kill -9 1234

This sends:

SIGKILL (9)

This means:

"Terminate this process immediately."

The major difference is that the process cannot catch, handle, or ignore SIGKILL.

Conceptually:

SIGTERM
   ↓
Process gets a chance to clean up
   ↓
Exit gracefully

versus:

SIGKILL
   ↓
Process is forcibly terminated

So kill -9 should generally be treated as a last resort.

4. Simple comparison
| Command        | Signal       | Meaning                      | Can process handle it? | Typical use                |
| -------------- | ------------ | ---------------------------- | ---------------------- | -------------------------- |
| `kill PID`     | SIGTERM (15) | Graceful termination request | Yes                    | Normal shutdown            |
| `kill -15 PID` | SIGTERM (15) | Graceful termination request | Yes                    | Explicit graceful shutdown |
| `kill -9 PID`  | SIGKILL (9)  | Force termination            | **No**                 | Stuck/unresponsive process |


Imagine your application is running:

ps aux | grep myapp

You find:

PID = 4567

First, you would normally try:

kill 4567

Give the application an opportunity to shut down cleanly.

Check:

ps -p 4567

If it's still running and genuinely stuck, you might use:

kill -9 4567
6. Why not always use kill -9?

This is a very common interview follow-up.

You might say:

"kill -9 forcibly terminates the process and doesn't allow the application to perform its normal cleanup. Therefore, I would normally try SIGTERM first and use SIGKILL only when the process doesn't terminate or is otherwise stuck."

For example, imagine an application has:

Open database connection
Open file
Write pending logs
Process request

With SIGTERM, the application may have code to clean these things up.

With SIGKILL, the process is terminated without getting the opportunity to handle the signal.

7. Very important: kill doesn't necessarily mean "kill"

The command name can be misleading.

For example:

kill -15 1234

doesn't mean "immediately kill process 1234."

It means:

Send signal 15 to process 1234

You can see available signals with:

kill -l

You'll see signals such as:

SIGTERM
SIGKILL
SIGHUP
SIGINT
SIGSTOP
...
8. A DevOps interview scenario
Interviewer:

"Your production application is not responding. What would you do?"

A reasonable answer:

1. Identify the process.
2. Check its status/resource usage.
3. Try graceful termination with SIGTERM.
4. Verify whether it exited.
5. If it remains stuck, investigate further and, if appropriate,
   use SIGKILL as a last resort.

Commands could be:

ps aux | grep myapp

Then:

kill -15 <PID>

Check:

ps -p <PID>

If necessary:

kill -9 <PID>
⭐ Interview answer to memorize

If they ask:

"What's the difference between kill, kill -9 and kill -15?"

Say:

"kill PID sends SIGTERM (15) by default. SIGTERM asks the process to terminate gracefully, so the application can handle the signal and perform cleanup. kill -15 PID explicitly sends the same SIGTERM signal. kill -9 PID sends SIGKILL, which cannot be caught or handled by the process and forcibly terminates it. In production, I would normally try SIGTERM first and use SIGKILL only when necessary, such as when a process is stuck."

🧠 Easy memory trick
kill PID
   ↓
SIGTERM (15)
   ↓
"Please shut down gracefully."

kill -15 PID
   ↓
SIGTERM (15)
   ↓
"Please shut down gracefully."

kill -9 PID
   ↓
SIGKILL (9)
   ↓
"Stop immediately."

Interview golden rule:
15 = graceful, 9 = forceful.