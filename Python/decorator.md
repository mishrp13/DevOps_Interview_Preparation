```

This code defines two reusable decorators, timer and retry, and stacks them on a function that calls an API. (Your first line says mport; it should be import.)

Background: what is a decorator?

A decorator is a function that takes a function and returns a new, wrapped version of it. This:

python
@timer
def call_api(): ...

is shorthand for call_api = timer(call_api).

Imports
python
import functools, logging, time, random
functools provides wraps, which keeps the original function's name and docstring.
logging writes log messages.
time provides the clock and sleep.
random adds a small random delay (jitter).
The timer decorator
python
def timer(fn):

Takes the function to be wrapped (fn).

python
    @functools.wraps(fn)

Copies fn's metadata (__name__, __doc__) onto wrapper. Without it, every decorated function would show up as wrapper in logs and debugging.

python
    def wrapper(*args, **kwargs):

The replacement function. *args, **kwargs accept any arguments, so the decorator works on any function.

python
        start = time.perf_counter()

Records the start time using a high-resolution clock suited to measuring durations.

python
        try:
            return fn(*args, **kwargs)

Calls the real function with the same arguments and returns its result.

python
        finally:
            logging.info("%s took %.2fs", fn.__name__, time.perf_counter() - start)

finally always runs, whether fn returned normally or raised an exception. So the duration is logged even for failed calls. %.2f formats the time to 2 decimal places.

python
    return wrapper

Returns the wrapped function, which replaces the original.

The retry decorator

This one takes arguments, so it has three nested layers:

python
def retry(max_tries=3, base_delay=0.5, exceptions=(Exception,)):

Layer 1 receives the settings: maximum attempts, starting delay in seconds, and which exception types should trigger a retry (a tuple).

python
    def decorator(fn):

Layer 2 receives the function, like timer does.

python
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):

Layer 3 is the replacement function, again preserving metadata.

python
            for attempt in range(max_tries):

Loops attempt = 0, 1, 2, ... up to max_tries - 1.

python
                try:
                    return fn(*args, **kwargs)

Tries the call. On success it returns immediately and the loop ends.

python
                except exceptions as exc:

Catches only the exception types you listed. Anything else (such as ValueError) propagates at once with no retry.

python
                    if attempt == max_tries - 1:
                        raise

On the last attempt it gives up and re-raises the original exception, so the caller still sees the failure.

python
                    delay = base_delay * 2 ** attempt + random.random() * 0.1

This is exponential backoff with jitter. With base_delay=0.5, the waits are about 0.5s, 1s, 2s, 4s, each plus up to 0.1s of random noise. The growing delay gives a struggling service time to recover, and the jitter stops many clients from retrying at exactly the same moment.

python
                    logging.warning("%s failed (%s), retrying in %.1fs",
                                    fn.__name__, exc, delay)
                    time.sleep(delay)

Logs which function failed, the error, and the wait, then sleeps before the next attempt.

python
        return wrapper
    return decorator

Layer 3 returns wrapper to layer 2, and layer 2 returns decorator to layer 1's caller. This is what allows @retry(max_tries=5) to work.

Applying them
python
@retry(max_tries=5, exceptions=(ConnectionError, TimeoutError))
@timer
def call_api():
    ...
retry(...) runs first and returns a decorator, which is then applied.
Decorators apply bottom to top: timer wraps call_api first, then retry wraps the timed version. It is equivalent to call_api = retry(...)(timer(call_api)).
At call time the order is therefore: retry → timer → your function.
Up to 5 attempts are made, and only ConnectionError or TimeoutError trigger a retry.
Because timer is inside retry, each attempt is timed separately. If you swapped the order, you'd get one time covering all attempts including the sleeps.
The ... is Python's Ellipsis, a placeholder for the function body you'd write.

Example log output if the first two calls fail:

WARNING call_api failed (Connection reset), retrying in 0.5s
INFO    call_api took 0.31s
WARNING call_api failed (timed out), retrying in 1.0s
INFO    call_api took 5.00s
INFO    call_api took 0.42s     <- third attempt succeeded

Note that logging.info messages only appear if you configure logging, for example logging.basicConfig(level=logging.INFO). By default only warnings and above are shown.



```