```

•What is the GIL? Threading vs multiprocessing vs asyncio, and which would you use for I/O-bound tasks like calling 100 AWS APIs?


For a DevOps Python interview, this is a very important topic because automation often means doing many things at the same time: calling AWS APIs, checking servers, running commands, waiting for deployments, reading files, etc.

The key question is:

If I need to call 100 AWS APIs, how should I run them efficiently?

Let's break it down.

1. What is the GIL?

GIL = Global Interpreter Lock.

In CPython, the GIL allows only one thread at a time to execute Python bytecode within a process.

That means if you create:

import threading

# Thread 1
# Thread 2
# Thread 3

multiple threads can exist, but they don't execute Python bytecode truly in parallel on multiple CPU cores.

Why does this matter?

It matters mainly for CPU-bound tasks.

For example:

def calculate():
    for i in range(100000000):
        x = i * i

If you use multiple Python threads for this kind of work, the GIL prevents the threads from getting true parallel CPU execution in the usual CPython model.

2. Does the GIL prevent threading from being useful?

No.

This is a very important interview point.

The GIL does not mean:

"Never use threads."

Threads are very useful for I/O-bound tasks.

Why?

Because when a thread is waiting for I/O:

Python thread
     ↓
AWS API request
     ↓
WAITING................
     ↓
AWS response

Python can allow another thread to run while the first thread is waiting.

So for I/O:

Thread 1 → waiting for AWS
Thread 2 → calling AWS
Thread 3 → waiting for network
Thread 4 → calling AWS

This can dramatically improve throughput.

3. CPU-bound vs I/O-bound

This distinction is probably the most important thing to understand for the interview.

CPU-bound

The program spends most of its time doing computation.

Examples:

Compressing huge amounts of data
Image processing
Encryption
Large mathematical calculations
Parsing/processing huge datasets
CPU ████████████████████
I/O
I/O-bound

The program spends most of its time waiting.

Examples:

AWS API calls
HTTP requests
SSH connections
Database queries
Reading files
Waiting for external services
CPU ██
I/O ████████████████████

AWS API calls are generally I/O-bound.

4. Threading

Python's threading module allows multiple threads within one process.

Example:

import threading

def call_aws_api():
    print("Calling AWS API")

threads = []

for i in range(10):
    t = threading.Thread(target=call_aws_api)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

Conceptually:

             Python process
                  |
       ┌──────────┼──────────┐
       ↓          ↓          ↓
    Thread 1   Thread 2   Thread 3
       ↓          ↓          ↓
    AWS API    AWS API    AWS API
Good for:

I/O-bound tasks.

Examples:

100 AWS API calls
100 HTTP requests
100 SSH operations
Multiple database queries
5. Multiprocessing

multiprocessing creates separate processes.

Each process has its own Python interpreter and therefore its own GIL.

from multiprocessing import Pool

def calculate(x):
    return x * x

with Pool(4) as pool:
    results = pool.map(calculate, range(10))

Conceptually:

Process 1 → GIL 1 → CPU core
Process 2 → GIL 2 → CPU core
Process 3 → GIL 3 → CPU core
Process 4 → GIL 4 → CPU core

This allows actual parallel CPU execution.

Good for:

CPU-bound tasks.

For example:

Large calculation
     ↓
Process 1 → CPU
Process 2 → CPU
Process 3 → CPU
Process 4 → CPU
6. asyncio

asyncio uses asynchronous programming, generally with an event loop.

Instead of creating a thread for every operation, you can have one thread efficiently manage many I/O operations.

Example:

import asyncio

async def call_api():
    print("Calling API")
    await asyncio.sleep(1)
    print("API completed")

async def main():
    await asyncio.gather(
        call_api(),
        call_api(),
        call_api()
    )

asyncio.run(main())

The important keyword is:

await

When the operation is waiting, the event loop can work on another task.

Conceptually:

              Event Loop
                  |
       ┌──────────┼──────────┐
       ↓          ↓          ↓
    API call    API call    API call
       ↓          ↓          ↓
     await      await       await
       ↓          ↓          ↓
       └──────── Event Loop ──┘
7. Threading vs multiprocessing vs asyncio

For interviews, memorize this:

| Approach          | Best for        |                   Parallel CPU? | Example         |
| ----------------- | --------------- | ------------------------------: | --------------- |
| `threading`       | I/O-bound       |                    ❌ Usually no | AWS/HTTP/SSH    |
| `multiprocessing` | CPU-bound       |                           ✅ Yes | Data processing |
| `asyncio`         | High-volume I/O | ❌ Usually one event-loop thread | APIs/network    |


The important word is usually because the exact behavior depends on the implementation and workload.

8. Your example: 100 AWS API calls

Suppose you have:

for instance in instances:
    response = aws_client.describe_instances(...)

If you make them sequentially:

API 1 ────────┐
              ↓
API 2 ────────┐
              ↓
API 3 ────────┐
              ↓
...
API 100 ──────┐

If each request takes ~1 second, the total can be roughly:

100 × 1 sec = 100 sec

The actual timing will vary, but the point is that you're waiting for each request before starting the next.

9. Using threads

You could use:

from concurrent.futures import ThreadPoolExecutor

def call_aws(instance_id):
    return aws_client.describe_instances(
        InstanceIds=[instance_id]
    )

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(
        executor.map(call_aws, instance_ids)
    )

Now several requests can be in flight concurrently.

Conceptually:

10 workers
 ↓
API 1  API 2  API 3 ... API 10
 ↓
wait for responses
 ↓
next batch

This is a very reasonable answer for a DevOps interview.

10. But there's an important AWS detail

Don't say:

"I'll create 100 threads because I have 100 APIs."

That's not necessarily a good design.

AWS APIs have:

API-specific rate limits
throttling
retries
network latency
service quotas

So you want controlled concurrency.

For example:

ThreadPoolExecutor(max_workers=10)

might be more sensible than:

ThreadPoolExecutor(max_workers=100)

The optimal number depends on the AWS service, API limits, request latency, and workload.

You should also think about exponential backoff/retries for throttling.

11. What about asyncio for AWS?

This is where a good candidate can stand out.

You might say:

"For 100 AWS API calls, I'd first consider whether the AWS SDK I'm using provides an appropriate asynchronous client. If I'm using the standard synchronous boto3 client, ThreadPoolExecutor is a straightforward approach for concurrent I/O. If I have an async-compatible AWS client and a larger amount of concurrent I/O, asyncio can be a good choice."

That's much better than blindly saying:

"AWS → asyncio."

Because the client library matters.

12. Why not multiprocessing for AWS API calls?

Because AWS API calls are mostly waiting on the network.

Using multiprocessing would introduce unnecessary overhead:

Main process
   ↓
Create processes
   ↓
Each process has interpreter
   ↓
Make network request
   ↓
Wait

You don't need multiple CPU processes just to sit around waiting for HTTP responses.

So:

AWS API calls → generally threading or asyncio, not multiprocessing.

13. A DevOps example

Imagine your script needs to check 100 EC2 instances:

Get instance 1 status
Get instance 2 status
Get instance 3 status
...
Get instance 100 status
Sequential
for instance in instances:
    check_instance(instance)

Simple but potentially slow.

Threading
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(check_instance, instances)

Good option when the SDK/API client is synchronous.

Asyncio

If you have an async-compatible client:

await asyncio.gather(
    check_instance(1),
    check_instance(2),
    check_instance(3),
    ...
)

Potentially very efficient for large-scale I/O.

14. Interview question: "Does GIL affect AWS API calls?"

A strong answer:

"The GIL is less of a concern for AWS API calls because they are I/O-bound. While a thread is waiting for a network response, another thread can execute. Therefore, Python threads can provide useful concurrency for AWS API calls even though the GIL prevents multiple threads from executing Python bytecode simultaneously in the usual CPython model."

That's a very good interview answer.

15. Interview question: "Threading or multiprocessing?"

Say:

"I choose based on whether the workload is I/O-bound or CPU-bound. For I/O-bound work such as AWS API calls, HTTP requests, SSH, or database queries, I'd generally use threading or asyncio. For CPU-bound work, I'd consider multiprocessing because separate processes can execute on multiple CPU cores."

16. Interview question: "Threading or asyncio?"

This is slightly more advanced.

Threading

Good when:

Existing library is synchronous
You want simple concurrent execution
You're working with boto3/synchronous clients
The amount of concurrency is moderate

Example:

ThreadPoolExecutor(max_workers=10)
Asyncio

Good when:

The libraries are async-compatible
You have lots of concurrent I/O
You want efficient management of many network operations
You're comfortable with async/await

Example:

await asyncio.gather(...)
17. One thing interviewers love: don't confuse concurrency and parallelism
Concurrency

Multiple tasks are in progress during the same period.

Example:

API 1 → waiting
API 2 → running
API 3 → waiting
API 4 → running
Parallelism

Multiple tasks are actually executing at the same time, typically on multiple CPU cores.

CPU 1 → Task A
CPU 2 → Task B
CPU 3 → Task C

For your AWS example, you're mainly interested in concurrency, not CPU parallelism.

18. Your interview cheat sheet

Memorize this:

                 GIL
                  │
       ┌──────────┴───────────┐
       │                      │
   CPU-bound               I/O-bound
       │                      │
       ↓                      ↓
multiprocessing       threading / asyncio
       │                      │
   CPU work              AWS / HTTP / SSH
If interviewer asks:

"What is GIL?"

"The Global Interpreter Lock in CPython allows only one thread at a time to execute Python bytecode within a process. It limits CPU-bound multithreading, but it doesn't prevent threads from being useful for I/O-bound work."

"100 AWS APIs — what would you use?"

"AWS API calls are I/O-bound, so I would use controlled concurrency. With a synchronous AWS SDK such as boto3, ThreadPoolExecutor is a straightforward choice. If I have an async-compatible client and need high concurrency, I'd consider asyncio. I would also limit concurrency and handle AWS throttling with retries and exponential backoff."

"Why not multiprocessing?"

"Because the workload is network I/O rather than CPU computation. Multiprocessing adds process overhead without providing much benefit for simply waiting on API responses."

That last answer is particularly useful in a DevOps/SRE interview, because it shows you're thinking about not just Python syntax, but API limits, reliability, concurrency, and production behavior.