import logging as _logging
import time
from typing import Any

import httpx

from .response_wrapper import ResponseWrapper

_logger = _logging.getLogger("apitestgenie")


def _request_with_retry(
    method: str,
    url: str,
    retries: int = 0,
    retry_delay: int | float = 0,
    retry_on_status: list[int] | None = None,
    timeout: int | float | None = None,
    retry_backoff: bool = False,
    log_enabled: bool = False,
    **kwargs: Any,
) -> ResponseWrapper:
    attempt = 0

    while True:
        try:
            response = httpx.request(
                method,
                url,
                timeout=timeout,
                **kwargs
            )

            if log_enabled:
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


# --------------------------------------------------------
# SIMPLE MODE HTTP METHODS
# --------------------------------------------------------

def get(
    url: str,
    retries: int = 0,
    retry_delay: int | float = 0,
    retry_on_status: list[int] | None = None,
    timeout: int | float | None = None,
    retry_backoff: bool = False,
    logging: bool = False,
    **kwargs: Any,
) -> ResponseWrapper:
    return _request_with_retry(
        "GET", url,
        retries=retries,
        retry_delay=retry_delay,
        retry_on_status=retry_on_status,
        timeout=timeout,
        retry_backoff=retry_backoff,
        log_enabled=logging,
        **kwargs
    )


def post(
    url: str,
    json: Any = None,
    retries: int = 0,
    retry_delay: int | float = 0,
    retry_on_status: list[int] | None = None,
    timeout: int | float | None = None,
    retry_backoff: bool = False,
    logging: bool = False,
    **kwargs: Any,
) -> ResponseWrapper:
    return _request_with_retry(
        "POST", url,
        retries=retries,
        retry_delay=retry_delay,
        retry_on_status=retry_on_status,
        timeout=timeout,
        retry_backoff=retry_backoff,
        log_enabled=logging,
        json=json,
        **kwargs
    )


def put(
    url: str,
    json: Any = None,
    retries: int = 0,
    retry_delay: int | float = 0,
    retry_on_status: list[int] | None = None,
    timeout: int | float | None = None,
    retry_backoff: bool = False,
    logging: bool = False,
    **kwargs: Any,
) -> ResponseWrapper:
    return _request_with_retry(
        "PUT", url,
        retries=retries,
        retry_delay=retry_delay,
        retry_on_status=retry_on_status,
        timeout=timeout,
        retry_backoff=retry_backoff,
        log_enabled=logging,
        json=json,
        **kwargs
    )


def patch(
    url: str,
    json: Any = None,
    retries: int = 0,
    retry_delay: int | float = 0,
    retry_on_status: list[int] | None = None,
    timeout: int | float | None = None,
    retry_backoff: bool = False,
    logging: bool = False,
    **kwargs: Any,
) -> ResponseWrapper:
    return _request_with_retry(
        "PATCH", url,
        retries=retries,
        retry_delay=retry_delay,
        retry_on_status=retry_on_status,
        timeout=timeout,
        retry_backoff=retry_backoff,
        log_enabled=logging,
        json=json,
        **kwargs
    )


def delete(
    url: str,
    retries: int = 0,
    retry_delay: int | float = 0,
    retry_on_status: list[int] | None = None,
    timeout: int | float | None = None,
    retry_backoff: bool = False,
    logging: bool = False,
    **kwargs: Any,
) -> ResponseWrapper:
    return _request_with_retry(
        "DELETE", url,
        retries=retries,
        retry_delay=retry_delay,
        retry_on_status=retry_on_status,
        timeout=timeout,
        retry_backoff=retry_backoff,
        log_enabled=logging,
        **kwargs
    )


def head(
    url: str,
    retries: int = 0,
    retry_delay: int | float = 0,
    retry_on_status: list[int] | None = None,
    timeout: int | float | None = None,
    retry_backoff: bool = False,
    logging: bool = False,
    **kwargs: Any,
) -> ResponseWrapper:
    return _request_with_retry(
        "HEAD", url,
        retries=retries,
        retry_delay=retry_delay,
        retry_on_status=retry_on_status,
        timeout=timeout,
        retry_backoff=retry_backoff,
        log_enabled=logging,
        **kwargs
    )


def options(
    url: str,
    retries: int = 0,
    retry_delay: int | float = 0,
    retry_on_status: list[int] | None = None,
    timeout: int | float | None = None,
    retry_backoff: bool = False,
    logging: bool = False,
    **kwargs: Any,
) -> ResponseWrapper:
    return _request_with_retry(
        "OPTIONS", url,
        retries=retries,
        retry_delay=retry_delay,
        retry_on_status=retry_on_status,
        timeout=timeout,
        retry_backoff=retry_backoff,
        log_enabled=logging,
        **kwargs
    )
