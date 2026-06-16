# APItestGenie

APItestGenie is a lightweight, developer-friendly Python library designed to simplify API testing for automation engineers.

---

## Overview

APItestGenie provides:

- Two ways to perform API requests: Client mode and Simple mode
- Built-in JSON assertions and JSON path assertions for nested responses
- Header assertions
- Response time assertions
- JSON schema validation (optional)
- Retry logic with fixed or exponential backoff delay
- Optional request logging
- GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS support
- Timeout and headers support
- A complete pytest suite
- A modern Python packaging layout using the src structure

---

## Installation

Clone the repository:

```
git clone https://github.com/Akash402/apitestgenie.git
cd apitestgenie
```

Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```
pip install httpx pytest
```

(Optional) Install the library locally in editable mode:

```
pip install -e .
```

For JSON schema validation support:

```
pip install apitestgenie[schema]
```

---

## Usage Examples

### Client Mode

```python
from apitestgenie.client import ApiClient

api = ApiClient("https://jsonplaceholder.typicode.com", timeout=10)

response = api.get("/posts/1", retries=2)
response.assert_status(200)
response.assert_json_value("id", 1)
```

POST example:

```python
resp = api.post("/posts", json={"title": "foo"})
resp.assert_status(201)
```

PUT example:

```python
resp = api.put("/posts/1", json={"id": 1, "title": "updated"})
resp.assert_status(200)
```

DELETE example:

```python
resp = api.delete("/posts/1")
resp.assert_status(200)
```

HEAD and OPTIONS example:

```python
resp = api.head("/posts/1")
resp.assert_status(200)

resp = api.options("/posts/1")
assert resp.status_code in (200, 204)
```

---

### Simple Mode

```python
from apitestgenie.simple import get

response = get("https://jsonplaceholder.typicode.com/posts/1")
response.assert_status(200)
print(response.json())
```

POST example:

```python
from apitestgenie.simple import post

resp = post("https://jsonplaceholder.typicode.com/posts", json={"hello": "world"})
resp.assert_status(201)
```

HEAD and OPTIONS example:

```python
from apitestgenie.simple import head, options

resp = head("https://jsonplaceholder.typicode.com/posts/1")
resp.assert_status(200)

resp = options("https://jsonplaceholder.typicode.com/posts/1")
assert resp.status_code in (200, 204)
```

Retry and timeout example:

```python
resp = get(
    "https://jsonplaceholder.typicode.com/posts/1",
    retries=3,
    retry_delay=1,
    retry_on_status=[500],
    timeout=5
)
```

---

## JSON Assertions

```python
resp.assert_status(200)
resp.assert_json_key("id")
resp.assert_json_value("id", 1)
resp.assert_json_path_exists("user.address.city")
resp.assert_json_path_value("user.address.city", "London")
```

---

## Header Assertions

```python
resp.assert_header("content-type")
resp.assert_header_value("content-type", "application/json")
```

Header name matching is case-insensitive.

---

## Response Time Assertion

```python
resp.assert_response_time(2.0)  # fails if response took more than 2 seconds
```

---

## JSON Schema Validation

Requires `jsonschema` (`pip install apitestgenie[schema]`):

```python
schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"}
    },
    "required": ["id"]
}
resp.assert_json_schema(schema)
```

---

## Retry with Exponential Backoff

```python
resp = api.get(
    "/posts/1",
    retries=3,
    retry_delay=1,
    retry_on_status=[503],
    retry_backoff=True   # sleeps 2s, 4s, 8s between retries
)
```

Without `retry_backoff=True` (default), the delay is fixed at `retry_delay` seconds.

---

## Logging

Pass `logging=True` to emit `INFO`-level log lines for each request (method, URL, status, elapsed):

```python
import logging
logging.basicConfig(level=logging.INFO)

api = ApiClient("https://jsonplaceholder.typicode.com", logging=True)
api.get("/posts/1")
# INFO apitestgenie: GET https://jsonplaceholder.typicode.com/posts/1 -> 200 (0.123s)
```

In simple mode:

```python
get("https://jsonplaceholder.typicode.com/posts/1", logging=True)
```

Logging is off by default.

---

## Chaining Assertions

All assertion methods return `self`, so they can be chained:

```python
api.get("/posts/1") \
    .assert_status(200) \
    .assert_response_time(2.0) \
    .assert_header("content-type") \
    .assert_json_key("id") \
    .assert_json_value("id", 1)
```

---

## Running Tests

```
pytest
```

---

## Project Structure

```
apitestgenie/
│
├── src/
│   └── apitestgenie/
│       ├── client.py
│       ├── simple.py
│       ├── response_wrapper.py
│       └── __init__.py
│
├── tests/
├── playground.py
├── pytest.ini
├── README.md
└── SCOPE.md
```

---

## Changelog

### v1.1.0

- Added `assert_header(name)` and `assert_header_value(name, expected)` to `ResponseWrapper`
- Added `assert_response_time(max_seconds)` to `ResponseWrapper`
- Added `assert_json_schema(schema)` to `ResponseWrapper` (requires `jsonschema`)
- Added `retry_backoff=True` option for exponential backoff on retries
- Added optional `logging=True` parameter on `ApiClient` and all simple mode functions
- Added `head()` and `options()` to both `ApiClient` and simple mode

### v1.0.0

- Initial release with GET, POST, PUT, PATCH, DELETE
- JSON and JSON path assertions
- Basic retry logic
- ResponseWrapper abstraction
- Client and simple modes

---

## License

MIT License. See [LICENSE](LICENSE) for details.
