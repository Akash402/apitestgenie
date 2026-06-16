import logging as _logging
import time
from typing import Any, Self

import httpx

from .response_wrapper import ResponseWrapper

_logger = _logging.getLogger("apitestgenie")


class ApiClient:
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str] | None = None,
        timeout: int | float = 30,
        logging: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = httpx.Client(headers=headers, timeout=timeout)
        self._log_enabled = logging

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request_with_retry(
        self,
        method: str,
        url: str,
        retries: int,
        retry_delay: int | float,
        retry_on_status: list[int] | None,
        retry_backoff: bool = False,
        **kwargs: Any,
    ) -> ResponseWrapper:
        attempt = 0

        while True:
            try:
                response = self.session.request(method, url, **kwargs)

                if self._log_enabled:
                    elapsed = response.elapsed.total_seconds()
                    _logger.info("%s %s -> %s (%.3fs)", method, url, response.status_code, elapsed)

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

                delay = retry_delay * (2 ** attempt) if retry_backoff else retry_delay
                time.sleep(delay)

            except httpx.RequestError:
                attempt += 1
                if attempt > retries:
                    raise
                delay = retry_delay * (2 ** attempt) if retry_backoff else retry_delay
                time.sleep(delay)

    # ------------------------
    # HTTP METHODS
    # ------------------------

    def get(self, path: str, retries: int = 0, retry_delay: int | float = 0, retry_on_status: list[int] | None = None, retry_backoff: bool = False, **kwargs: Any) -> ResponseWrapper:
        url = self._build_url(path)
        return self._request_with_retry("GET", url, retries, retry_delay, retry_on_status, retry_backoff, **kwargs)

    def post(self, path: str, json: Any = None, retries: int = 0, retry_delay: int | float = 0, retry_on_status: list[int] | None = None, retry_backoff: bool = False, **kwargs: Any) -> ResponseWrapper:
        url = self._build_url(path)
        return self._request_with_retry("POST", url, retries, retry_delay, retry_on_status, retry_backoff, json=json, **kwargs)

    def put(self, path: str, json: Any = None, retries: int = 0, retry_delay: int | float = 0, retry_on_status: list[int] | None = None, retry_backoff: bool = False, **kwargs: Any) -> ResponseWrapper:
        url = self._build_url(path)
        return self._request_with_retry("PUT", url, retries, retry_delay, retry_on_status, retry_backoff, json=json, **kwargs)

    def patch(self, path: str, json: Any = None, retries: int = 0, retry_delay: int | float = 0, retry_on_status: list[int] | None = None, retry_backoff: bool = False, **kwargs: Any) -> ResponseWrapper:
        url = self._build_url(path)
        return self._request_with_retry("PATCH", url, retries, retry_delay, retry_on_status, retry_backoff, json=json, **kwargs)

    def delete(self, path: str, retries: int = 0, retry_delay: int | float = 0, retry_on_status: list[int] | None = None, retry_backoff: bool = False, **kwargs: Any) -> ResponseWrapper:
        url = self._build_url(path)
        return self._request_with_retry("DELETE", url, retries, retry_delay, retry_on_status, retry_backoff, **kwargs)

    def head(self, path: str, retries: int = 0, retry_delay: int | float = 0, retry_on_status: list[int] | None = None, retry_backoff: bool = False, **kwargs: Any) -> ResponseWrapper:
        url = self._build_url(path)
        return self._request_with_retry("HEAD", url, retries, retry_delay, retry_on_status, retry_backoff, **kwargs)

    def options(self, path: str, retries: int = 0, retry_delay: int | float = 0, retry_on_status: list[int] | None = None, retry_backoff: bool = False, **kwargs: Any) -> ResponseWrapper:
        url = self._build_url(path)
        return self._request_with_retry("OPTIONS", url, retries, retry_delay, retry_on_status, retry_backoff, **kwargs)

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
