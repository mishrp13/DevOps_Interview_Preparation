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



@monitor
def deploy(environment):
    print(f"Deploying to {environment}")
    time.sleep(2)
    return "SUCCESS"



deploy("production")