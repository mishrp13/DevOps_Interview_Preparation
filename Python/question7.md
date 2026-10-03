```

What are decorators? Write one (timer, retry, logging)


For a Python + DevOps interview, decorators are important because they let you add behavior to existing functions without changing the function's core code.

In DevOps, a decorator can be useful for things like:

Logging
Retry logic for flaky API/network calls
Measuring execution time
Authentication/authorization
Monitoring
Error handling
1. What is a decorator?

A decorator is a function that takes another function as input, adds some behavior, and returns a modified function.

Think:

Original function
      ↓
   Decorator
      ↓
Function with extra behavior

For example, suppose you have:

def deploy():
    print("Deploying application...")

You don't want to modify deploy() itself, but you want logging around it.

A decorator can do that.

2. Simple logging decorator
def logger(func):
    def wrapper():
        print("Starting function...")
        func()
        print("Function completed!")

    return wrapper

Now apply it:

@logger
def deploy():
    print("Deploying application...")

When you call:

deploy()

Output:

Starting function...
Deploying application...
Function completed!

The important syntax is:

@logger

This:

@logger
def deploy():
    ...

is essentially equivalent to:

def deploy():
    ...

deploy = logger(deploy)

That's a very common interview question.

3. Why use decorators in DevOps?

Imagine you have 20 automation functions:

deploy()
restart_server()
backup_database()
check_health()
update_config()

You want to log when each function starts and finishes.

Without decorators, you might repeatedly write:

def deploy():
    print("Starting deploy")
    # deployment logic
    print("Finished deploy")


def restart_server():
    print("Starting restart")
    # restart logic
    print("Finished restart")

That's repetitive.

Instead:

@logger
def deploy():
    # deployment logic
    pass


@logger
def restart_server():
    # restart logic
    pass

The logging behavior is centralized in one place.

4. DevOps example: Retry decorator ⭐

This is particularly useful in DevOps.

Network operations can fail temporarily:

API request
    ↓
Connection timeout
    ↓
retry
    ↓
success

You could create a retry decorator:

import time

def retry(func):
    def wrapper():
        for attempt in range(3):
            try:
                return func()
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2)

        print("All attempts failed")

    return wrapper

Use it:

@retry
def deploy():
    print("Deploying...")
    # Imagine this sometimes fails
    raise Exception("Server unavailable")

Call:

deploy()

You might get:

Deploying...
Attempt 1 failed: Server unavailable
Deploying...
Attempt 2 failed: Server unavailable
Deploying...
Attempt 3 failed: Server unavailable
All attempts failed

This is a realistic DevOps use case for transient failures in things like API calls or infrastructure operations.

5. Timer decorator

Another common interview example is measuring how long an operation takes.

import time

def timer(func):
    def wrapper():
        start = time.time()

        func()

        end = time.time()

        print(f"Execution time: {end - start:.2f} seconds")

    return wrapper

Apply it:

@timer
def deploy():
    time.sleep(2)
    print("Deployment completed")

Call:

deploy()

Output:

Deployment completed
Execution time: 2.00 seconds

This can be useful for measuring:

Deployment duration
Backup duration
API response time
Script execution time
Infrastructure automation tasks
6. Important interview issue: *args and **kwargs

The previous examples only work with functions that don't require arguments.

But what if we have:

@timer
def deploy(environment, version):
    ...

Then our decorator should be flexible.

Use:

import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        print(f"Execution time: {end - start:.2f} seconds")

        return result

    return wrapper

Now:

@timer
def deploy(environment, version):
    print(f"Deploying {version} to {environment}")
    time.sleep(1)
    return "SUCCESS"

Call:

result = deploy("production", "v2.1")
print(result)

Output:

Deploying v2.1 to production
Execution time: 1.00 seconds
SUCCESS
Why *args and **kwargs?

Because the decorator doesn't know beforehand what arguments the original function accepts.

func(*args, **kwargs)

passes those arguments through to the original function.

This connects directly to the *args / **kwargs question you asked earlier.

7. Very important: functools.wraps

A good production-quality decorator should generally use functools.wraps.

from functools import wraps
import time

def timer(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        print(f"{func.__name__} took {end - start:.2f} seconds")

        return result

    return wrapper

Why?

Without @wraps, the wrapper can replace useful metadata such as the original function's name and docstring.

8. A strong DevOps interview example

Here's a practical version combining logging + timing:

from functools import wraps
import time

def monitor(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        print(f"Starting: {func.__name__}")

        start = time.time()

        try:
            result = func(*args, **kwargs)
            print(f"{func.__name__} completed successfully")
            return result

        except Exception as e:
            print(f"{func.__name__} failed: {e}")
            raise

        finally:
            elapsed = time.time() - start
            print(f"Execution time: {elapsed:.2f}s")

    return wrapper

Use it:

@monitor
def deploy(environment):
    print(f"Deploying to {environment}")
    time.sleep(2)
    return "SUCCESS"

Call:

deploy("production")

Possible output:

Starting: deploy
Deploying to production
deploy completed successfully
Execution time: 2.00s

If deployment fails:

Starting: deploy
Deploying to production
deploy failed: Connection timeout
Execution time: 2.00s

The decorator handles the cross-cutting behavior, while deploy() contains only deployment logic.

⭐ Interview answer

If the interviewer asks:

"What are decorators in Python?"

A strong answer is:

"A decorator is a function that takes another function, adds additional behavior to it, and returns a modified function. It allows us to add functionality without changing the original function's code. In DevOps, decorators can be useful for logging, retrying transient failures, measuring execution time, authentication, and monitoring automation functions."

Then show:

from functools import wraps
import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        print(f"Execution time: {time.time() - start:.2f}s")

        return result

    return wrapper


@timer
def deploy(environment):
    print(f"Deploying to {environment}")
    time.sleep(2)


deploy("production")
Remember this flow
@timer
   ↓
timer(deploy)
   ↓
wrapper()
   ↓
start timer
   ↓
call deploy()
   ↓
stop timer
   ↓
return result

One-line memory trick:

Decorator = add behavior to a function without modifying its actual code.

And for a DevOps interview, retry + logging + timing are the three examples I'd be prepared to explain.