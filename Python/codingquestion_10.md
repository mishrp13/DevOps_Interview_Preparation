```

Call a REST API with retries, timeout and exponential backoff (requests) ?

Interview-ready Python script



import requests
import time

def call_api(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)

            # Retry for server errors
            if response.status_code >= 500:
                raise requests.exceptions.HTTPError(
                    f"Server error: {response.status_code}"
                )

            # Raise error for other HTTP failures
            response.raise_for_status()

            print("API call successful!")
            return response.json()

        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError) as e:

            print(f"Attempt {attempt + 1} failed: {e}")

            # Don't retry client errors like 400 or 404
            if isinstance(e, requests.exceptions.HTTPError):
                if response.status_code < 500:
                    raise

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    print("All retries failed!")
    return None


# Main program
url = "https://jsonplaceholder.typicode.com/posts/1"

result = call_api(url)

if result:
    print(result)


Install the required library:

pip install requests

Understand the script step by step
Concept	              Explanation
requests.get()	      Calls the REST API using HTTP GET
timeout=5	          Prevents a request from waiting indefinitely
max_retries=3	      Allows up to 3 total attempts
try/except	          Handles network and HTTP errors
response.raise_for_status()	Raises an exception for 4xx and 5xx responses
2 ** attempt	     Calculates exponential backoff
time.sleep()	     Waits before retrying

The retry delays increase exponentially: 1 second, 2 seconds, 4 seconds, 8 seconds... for longer retry sequences.

This reduces pressure on an API during temporary outages.

Example output
Suppose the API is temporarily unavailable:

Attempt 1 failed: Server error: 503
Retrying in 1 seconds...

Attempt 2 failed: Server error: 503
Retrying in 2 seconds...

API call successful!

{'userId': 1, 'id': 1, 'title': '...', 'body': '...'}


How to explain it in a DevOps interview
Interviewer: How do you call a REST API with retries, timeout, and exponential backoff in Python?

Your answer:
I use the Python requests library to call REST APIs. I set a timeout so the request doesn't hang indefinitely. I implement retry logic using a for loop and exception handling. If the API fails due to a temporary server error, timeout, or connection issue, I retry using exponential backoff with the formula 2 to the power of the attempt number. I avoid retrying normal client errors like 400 and 404. This improves reliability when dealing with temporary network or server failures.