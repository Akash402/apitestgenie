import httpx
from .response_wrapper import ResponseWrapper

def get(url, **kwargs):
    return ResponseWrapper(httpx.get(url, **kwargs))

def post(url, json=None, **kwargs):
    return ResponseWrapper(httpx.post(url, json=json, **kwargs))

def put(url, json=None, **kwargs):
    return ResponseWrapper(httpx.put(url, json=json, **kwargs))

def patch(url, json=None, **kwargs):
    return ResponseWrapper(httpx.patch(url, json=json, **kwargs))

def delete(url, **kwargs):
    return ResponseWrapper(httpx.delete(url, **kwargs))
