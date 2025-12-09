import time
import httpx
from .response_wrapper import ResponseWrapper


class ApiClient:
    def __init__(self, base_url, headers=None, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.session = httpx.Client(headers=headers, timeout=timeout)

    def _build_url(self, path):
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request_with_retry(self, method, url, retries, retry_delay, retry_on_status, **kwargs):
        attempt = 0

        while True:
            try:
                response = self.session.request(method, url, **kwargs)

                # If no retry rules → return immediately
                if not retry_on_status:
                    return ResponseWrapper(response)

                # If status code NOT in retry list → return
                if response.status_code not in retry_on_status:
                    return ResponseWrapper(response)

                # If retry limit exceeded → return last response
                attempt += 1
                if attempt > retries:
                    return ResponseWrapper(response)

                time.sleep(retry_delay)

            except httpx.RequestError:
                attempt += 1
                if attempt > retries:
                    raise
                time.sleep(retry_delay)

    # ------------------------
    # HTTP METHODS
    # ------------------------

    def get(self, path, retries=0, retry_delay=0, retry_on_status=None, **kwargs):
        url = self._build_url(path)
        return self._request_with_retry("GET", url, retries, retry_delay, retry_on_status, **kwargs)

    def post(self, path, json=None, retries=0, retry_delay=0, retry_on_status=None, **kwargs):
        url = self._build_url(path)
        return self._request_with_retry("POST", url, retries, retry_delay, retry_on_status, json=json, **kwargs)

    def put(self, path, json=None, retries=0, retry_delay=0, retry_on_status=None, **kwargs):
        url = self._build_url(path)
        return self._request_with_retry("PUT", url, retries, retry_delay, retry_on_status, json=json, **kwargs)

    def patch(self, path, json=None, retries=0, retry_delay=0, retry_on_status=None, **kwargs):
        url = self._build_url(path)
        return self._request_with_retry("PATCH", url, retries, retry_delay, retry_on_status, json=json, **kwargs)

    def delete(self, path, retries=0, retry_delay=0, retry_on_status=None, **kwargs):
        url = self._build_url(path)
        return self._request_with_retry("DELETE", url, retries, retry_delay, retry_on_status, **kwargs)
