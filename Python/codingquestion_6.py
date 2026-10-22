
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

        response= requests.get(url,timeout=5)

        if 200 <= response.status_code <400:
            return f"Healthy: {url}- {response.status_code}"

        else:
            return f"Unhealthy: {url}- {response.status_code}"

    except requests.exceptions as error:
        return f"unhealthy: {url}- {error}"

with ThreadPoolExecutor(max_workers=10) as executor:
    results= executor.map(check_url,urls)

for result in results:
    print(result)
