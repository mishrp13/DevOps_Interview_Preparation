```

•How does exception handling work (try/except/else/finally)? How do you create custom exceptions?

For a Python + DevOps interview, exception handling is important because automation scripts must fail predictably, clean up resources, and provide useful error messages.

The key things to understand are:

try → code that might fail
except → handle the failure
else → runs if there was no exception
finally → runs no matter what
raise → deliberately raise an exception
Custom exception → define your own meaningful error type

1. What is exception handling?

An exception is an error/event that interrupts the normal execution of a program.

Example:

result = 10 / 0

This produces:

ZeroDivisionError: division by zero

Without handling it, the program stops.

With exception handling:

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")

Output:

Cannot divide by zero

The program can continue.

2. try / except

Basic structure:

try:
    # risky code
except:
    # handle error

Example:

try:
    response = call_aws_api()
except Exception as e:
    print(f"AWS API failed: {e}")

In DevOps automation, risky operations might include:

AWS API calls
SSH connections
File operations
Database queries
Configuration parsing
Subprocess execution
Network requests
3. Don't use a bare except

Avoid:

try:
    deploy()
except:
    print("Something went wrong")

Why?

Because it catches almost everything and hides the actual problem.

Prefer:

try:
    deploy()
except ConnectionError as e:
    print(f"Connection failed: {e}")

Or, when appropriate:

try:
    deploy()
except Exception as e:
    print(f"Deployment failed: {e}")

For production DevOps scripts, specific exceptions are generally better.

4. Multiple except blocks

You can handle different failures differently:

try:
    response = call_api()
except ConnectionError:
    print("Network connection failed")
except TimeoutError:
    print("API request timed out")
except PermissionError:
    print("Permission denied")

This is useful in automation because different failures may require different actions.

For example:

ConnectionError → retry
TimeoutError    → retry
PermissionError → don't retry, alert
5. else

The else block executes only if the try block succeeds without an exception.

Example:

try:
    result = deploy()
except Exception as e:
    print(f"Deployment failed: {e}")
else:
    print("Deployment completed successfully")

Flow:

             try
              |
       ┌──────┴──────┐
       |             |
    success        error
       |             |
      else         except
       |
     continue
Why use else?

It lets you keep the code that depends on successful execution separate from the error-handling code.

6. finally

finally runs regardless of whether an exception occurred.

Example:

try:
    deploy()
except Exception as e:
    print(f"Deployment failed: {e}")
finally:
    print("Cleaning up")

If deployment succeeds:

Deployment completed
Cleaning up

If deployment fails:

Deployment failed: ...
Cleaning up

This makes finally extremely useful for cleanup.

7. DevOps example: SSH connection

Imagine you're automating an SSH operation:

connection = None

try:
    connection = connect_to_server()
    run_command(connection)
except ConnectionError as e:
    print(f"SSH failed: {e}")
finally:
    if connection:
        connection.close()

The important point is:

Even if run_command() fails, the connection should still be closed.

This is exactly the kind of situation where finally is useful.

8. Complete try/except/else/finally

You can combine all four:

try:
    print("Connecting to server")
    result = deploy()

except ConnectionError as e:
    print(f"Connection failed: {e}")

except Exception as e:
    print(f"Deployment failed: {e}")

else:
    print("Deployment succeeded")

finally:
    print("Cleaning up deployment resources")

The execution flow is:

try
 │
 ├── exception? ── Yes ──> except
 │
 └── no exception ───────> else
                             
finally
   ↓
always executes
9. raise — deliberately raising an exception

You can create an exception yourself using raise.

Example:

environment = "testing"

if environment not in ["dev", "staging", "production"]:
    raise ValueError("Invalid environment")

Output:

ValueError: Invalid environment

This is very useful in DevOps scripts.

For example:

def deploy(environment):

    if environment not in ["dev", "staging", "production"]:
        raise ValueError(
            f"Invalid environment: {environment}"
        )

    print(f"Deploying to {environment}")

Now:

deploy("production")

works.

But:

deploy("abc")

raises:

ValueError: Invalid environment: abc
10. Re-raising an exception

This is important because you've already used it in your decorator.

You had:

except Exception as e:
    print(f"{func.__name__} failed: {e}")
    raise

That final:

raise

means:

"I caught the exception, logged it, but I don't want to hide it. Raise the original exception again."

For example:

try:
    deploy()
except Exception as e:
    print(f"Deployment failed: {e}")
    raise

Output might include:

Deployment failed: connection refused

Traceback ...
ConnectionError: connection refused

This is good for DevOps because you can log the error and still make the pipeline fail.

11. Why is raise important in CI/CD?

Imagine:

try:
    deploy()
except Exception as e:
    print(f"Deployment failed: {e}")

If you don't re-raise, your script might finish successfully from the shell's perspective.

That can be dangerous.

For example:

Deployment failed!
       ↓
Exception swallowed
       ↓
Python exits normally
       ↓
CI/CD thinks job succeeded ❌

Instead:

try:
    deploy()
except Exception as e:
    print(f"Deployment failed: {e}")
    raise

Then:

Deployment failed
       ↓
Exception propagates
       ↓
Python exits non-zero
       ↓
CI/CD job fails ✅

That's a very good DevOps interview point.

12. Custom exceptions

Sometimes standard exceptions aren't descriptive enough.

You can create your own exception.

Example:

class DeploymentError(Exception):
    pass

Then:

raise DeploymentError("Deployment failed")

Handle it:

try:
    deploy()
except DeploymentError as e:
    print(f"Deployment error: {e}")
13. Why create custom exceptions?

Imagine your automation has different types of failures:

DeploymentError
ConfigurationError
AWSResourceError
HealthCheckError
RollbackError

This makes your code easier to understand and handle.

For example:

class DeploymentError(Exception):
    pass


class HealthCheckError(Exception):
    pass

Then:

try:
    deploy()

    if not health_check():
        raise HealthCheckError("Application health check failed")

except DeploymentError as e:
    print(f"Deployment failed: {e}")

except HealthCheckError as e:
    print(f"Health check failed: {e}")

Now your automation can distinguish between:

deployment failure
        vs
health check failure
14. Custom exception hierarchy

You can create a hierarchy:

class DevOpsError(Exception):
    pass


class DeploymentError(DevOpsError):
    pass


class HealthCheckError(DevOpsError):
    pass


class RollbackError(DevOpsError):
    pass

Now:

raise DeploymentError("Deployment failed")

can be caught specifically:

except DeploymentError:
    ...

or broadly:

except DevOpsError:
    ...

This is useful for larger automation frameworks.

15. Custom exception with additional information

You can also store useful information:

class DeploymentError(Exception):

    def __init__(self, environment, message):
        self.environment = environment
        self.message = message

        super().__init__(message)

Then:

raise DeploymentError(
    "production",
    "Health check failed"
)

You could access:

except DeploymentError as e:
    print(e.environment)
    print(e.message)

Output:

production
Health check failed

For a large DevOps automation framework, this can make errors much easier to diagnose.

16. Exception chaining — important interview topic

Suppose you catch one exception and want to raise a more meaningful exception.

try:
    response = call_aws()
except ConnectionError as e:
    raise DeploymentError(
        "Unable to contact AWS"
    ) from e

Now you have:

ConnectionError
      ↓
DeploymentError

The from e preserves the original cause.

This is called exception chaining.

It's useful when you want to expose a domain-specific error while retaining the underlying technical reason.

17. DevOps example: AWS deployment

Here's a realistic pattern:

class DeploymentError(Exception):
    pass


def deploy(environment):

    try:
        print(f"Deploying to {environment}")

        response = call_aws_api()

        if response["status"] != "success":
            raise DeploymentError(
                f"AWS deployment failed in {environment}"
            )

    except ConnectionError as e:
        raise DeploymentError(
            f"Could not connect to AWS for {environment}"
        ) from e

    else:
        print("Deployment completed successfully")

    finally:
        print("Cleaning up deployment resources")

The flow is:

deploy()
   │
   ↓
try AWS operation
   │
   ├── ConnectionError
   │       ↓
   │   DeploymentError
   │
   ├── Other exception
   │
   └── success
          ↓
        else
          ↓
       success log
          ↓
       finally
          ↓
       cleanup
18. finally vs context manager

Since you just learned context managers, there's a useful connection.

You might write:

try:
    resource = acquire_resource()
    use_resource(resource)
finally:
    release_resource(resource)

But Python provides context managers:

with acquire_resource() as resource:
    use_resource(resource)

The context manager handles the cleanup for you.

So in an interview, you can say:

"For one-off cleanup, finally is useful. When resource management follows a reusable pattern, I'd generally consider a context manager."

That's a nice answer.

19. Common interview mistakes
❌ Don't do this
try:
    deploy()
except:
    pass

This hides failures.

❌ Don't do this unnecessarily
try:
    x = 10 + 20
except Exception:
    ...

Don't use exception handling around code that can't reasonably fail.

❌ Don't swallow deployment failures
try:
    deploy()
except Exception as e:
    print(e)

If this is a CI/CD script, the job might incorrectly appear successful.

Better:

try:
    deploy()
except Exception as e:
    print(f"Deployment failed: {e}")
    raise
20. Interview cheat sheet

Memorize this:

| Keyword                 | Purpose                                 |
| ----------------------- | --------------------------------------- |
| `try`                   | Code that might raise an exception      |
| `except`                | Handle an exception                     |
| `else`                  | Runs only if `try` succeeds             |
| `finally`               | Runs regardless of success/failure      |
| `raise`                 | Explicitly raise an exception           |
| `raise` inside `except` | Re-raise original exception             |
| `Exception`             | Base class for most built-in exceptions |
| Custom exception        | Application/domain-specific error       |

Execution pattern
try
 │
 ├── error ──> except
 │
 └── success ─> else
                 │
                 ↓
              finally
                 ↑
          always executes
⭐ Strong DevOps interview answer

If they ask:

"Explain exception handling in Python."

You can say:

"Python uses try, except, else, and finally for exception handling. I put potentially failing operations in try, handle expected exceptions in except, use else for code that should run only after successful execution, and use finally for cleanup that must happen regardless of success or failure. I can use raise to explicitly raise an exception and create custom exception classes by inheriting from Exception. In DevOps automation, I use this particularly for AWS API calls, SSH operations, file handling, and deployments. For CI/CD, I also make sure I don't swallow deployment errors; if I log an exception and still want the pipeline to fail, I re-raise it with raise."

The one DevOps point I'd especially remember:
except Exception as e:
    print(f"Deployment failed: {e}")
    raise

Log it + re-raise it → CI/CD can detect the failure.

That distinction between handling an error and silently swallowing an error is something interviewers often care about in automation code.