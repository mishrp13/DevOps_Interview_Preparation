
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
