
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
