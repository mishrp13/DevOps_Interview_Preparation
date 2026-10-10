```
Interview answer: I use Python's concurrent.futures.ThreadPoolExecutor to check multiple URLs concurrently. Each thread sends an HTTP request, checks the response status code, and reports whether the URL is healthy or unhealthy.
In DevOps, this is useful for monitoring application endpoints, microservices, websites, and health-check endpoints after deployment.
Python code — URL health check using threads
Install the dependency:
pip install requests


import requests
from concurrent.futures import ThreadPoolExecutor

urls = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.python.org",
    "https://httpbin.org/status/500"
]

def check_url(url):
    try:
        response = requests.get(url, timeout=5)

        if 200 <= response.status_code < 400:
            return f"HEALTHY: {url} - {response.status_code}"
        else:
            return f"UNHEALTHY: {url} - {response.status_code}"

    except requests.RequestException as error:
        return f"UNHEALTHY: {url} - {error}"

with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(check_url, urls)

for result in results:
    print(result)




How to explain the code in an interview
1. requests.get() — sends an HTTP GET request to the URL.
2. timeout=5 — prevents a request from waiting indefinitely.
3. Status code 200–399 — treated as healthy in this example; redirects count as healthy.
4. ThreadPoolExecutor(max_workers=10) — allows up to 10 requests to run concurrently.
5. executor.map() — schedules the URL checks and returns results in the original input order.
6. try-except — handles connection errors, DNS failures, and timeouts.
Example output
HEALTHY: https://www.google.com - 200
HEALTHY: https://www.github.com - 200
HEALTHY: https://www.python.org - 200
UNHEALTHY: https://httpbin.org/status/500 - 500


Actual results depend on network conditions and the endpoints' responses.
Common interview follow-up questions
Q1. Why use threads instead of sequential requests?
Because URL health checks are I/O-bound tasks. Threads can wait for multiple network requests concurrently, reducing total execution time.
Q2. Why use max_workers=10?
It limits concurrent requests and avoids overwhelming endpoints or consuming excessive resources. The ideal value depends on the number of URLs and service limits.
Q3. Why use a timeout?
To prevent slow or unresponsive endpoints from blocking the health-check script indefinitely.
Q4. What is the difference between threading and asyncio?
- ThreadPoolExecutor: straightforward for blocking libraries such as requests.
- asyncio: useful for large numbers of concurrent network requests when paired with an asynchronous HTTP client such as aiohttp or httpx.AsyncClient.
Q5. Is an HTTP 200 response enough to prove an application is healthy?
Not always. For production monitoring, you may also validate the response body, check a dedicated /health or /ready endpoint, enforce authentication where needed, and verify critical dependencies.
Interview tip: Start by explaining the problem, write the ThreadPoolExecutor solution, and then discuss timeouts, exception handling, HTTP status codes, and concurrency. This demonstrates practical Python automation skills for DevOps.