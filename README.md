# APItestGenie

APItestGenie is a lightweight, developer-friendly Python library designed to simplify API testing for automation engineers.
Version 1.0 focuses on clarity, correctness, and essential functionality without unnecessary complexity.

---

## Overview

APItestGenie provides:

- Two ways to perform API requests: Client mode and Simple mode
- Built-in JSON assertions
- JSON path assertions for nested responses
- Basic retry logic with retries, retry delay, and retry_on_status
- A ResponseWrapper abstraction for consistent behavior across requests
- GET, POST, PUT, PATCH, DELETE support
- Timeout and headers support
- A complete pytest suite
- A modern Python packaging layout using the src structure

Version 1.0 intentionally avoids heavy features like logging frameworks, async support, or automation framework integrations.

---

## Installation

Clone the repository:

```
git clone https://github.com/<yourname>/apitestgenie.git
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
resp.assert_json_path_exists("title")
resp.assert_json_path_value("id", 1)
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

## Version 1.0 Scope Summary

Included:

- CRUD operations
- Basic retry logic
- JSON and JSON path assertions
- ResponseWrapper abstraction
- Simple and client modes
- Header and timeout support
- Test suite
- Clean structure

Excluded:

- Advanced retry logic
- Logging framework
- Robot/Behave integrations
- Async support
- Schema validation
- Plugin system

---

## License

Add your license here (MIT recommended).
