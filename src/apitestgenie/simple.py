import time
import httpx
from .response_wrapper import ResponseWrapper

def _request_with_retry(
    method,
    url,
    retries=0,
    retry_delay=0,
    retry_on_status=None,
    timeout=None,
    **kwargs
):
    attempt = 0

    while True:
        try:
            response = httpx.request(
                method,
                url,
                timeout=timeout,
                **kwargs
            )

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

            # Otherwise retry
            time.sleep(retry_delay)

        except httpx.RequestError:
            attempt += 1
            if attempt > retries:
                raise
            time.sleep(retry_delay)


# --------------------------------------------------------
# SIMPLE MODE HTTP METHODS
# --------------------------------------------------------

def get(
    url,
    retries=0,
    retry_delay=0,
    retry_on_status=None,
    timeout=None,
    **kwargs
):
    return _request_with_retry(
        "GET", url,
        retries=retries,
        retry_delay=retry_delay,
        retry_on_status=retry_on_status,
        timeout=timeout,
        **kwargs
    )


def post(
    url,
    json=None,
    retries=0,
    retry_delay=0,
    retry_on_status=None,
    timeout=None,
    **kwargs
):
    return _request_with_retry(
        "POST", url,
        retries=retries,
        retry_delay=retry_delay,
        retry_on_status=retry_on_status,
        timeout=timeout,
        json=json,
        **kwargs
    )


def put(
    url,
    json=None,
    retries=0,
    retry_delay=0,
    retry_on_status=None,
    timeout=None,
    **kwargs
):
    return _request_with_retry(
        "PUT", url,
        retries=retries,
        retry_delay=retry_delay,
        retry_on_status=retry_on_status,
        timeout=timeout,
        json=json,
        **kwargs
    )


def patch(
    url,
    json=None,
    retries=0,
    retry_delay=0,
    retry_on_status=None,
    timeout=None,
    **kwargs
):
    return _request_with_retry(
        "PATCH", url,
        retries=retries,
        retry_delay=retry_delay,
        retry_on_status=retry_on_status,
        timeout=timeout,
        json=json,
        **kwargs
    )


def delete(
    url,
    retries=0,
    retry_delay=0,
    retry_on_status=None,
    timeout=None,
    **kwargs
):
    return _request_with_retry(
        "DELETE", url,
        retries=retries,
        retry_delay=retry_delay,
        retry_on_status=retry_on_status,
        timeout=timeout,
        **kwargs
    )
