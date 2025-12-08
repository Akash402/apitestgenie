import httpx
from .response_wrapper import ResponseWrapper

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = httpx.Client()

    def _build_url(self, path):
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path, **kwargs):
        response = self.session.get(self._build_url(path), **kwargs)
        return ResponseWrapper(response)
