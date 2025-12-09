# APItestGenie – Version 1.0 Scope Document  
A lightweight, developer-friendly Python library designed to simplify API testing for automation engineers.  
Version 1.0 focuses on stability, clarity, and essential functionality without unnecessary complexity.

---

# Version 1.0

Provide a **clean, minimal, reliable** API testing helper library that covers the needs of automation engineers using:

- Python directly  
- Pytest  
- Simple scripting  
- Frameworks like Robot / Behave (in future versions)

## 1. Core HTTP Methods
Support the essential HTTP verbs:

- `GET`
- `POST`
- `PUT`
- `PATCH`
- `DELETE`

All methods available via:
- **Client mode** (`ApiClient`)
- **Simple mode** (`get(url)`, `post(url)`, etc.)

---

## 2. Basic Retry Mechanism
Retries help automation engineers deal with flaky APIs.

Features included:

- `retries` — number of retry attempts  
- `retry_delay` — sleep between retries  
- `retry_on_status` — retry only on specific HTTP status codes  
- Retries occur on:  
  - network failures  
  - configurable status codes  

_Advanced retry logic is intentionally excluded from v1.0._

---

## 3. JSON Assertions
Built-in helpers for validating responses:

### Key-based assertions
- `assert_json_key(key)`
- `assert_json_value(key, expected)`

### JSON path assertions
Support nested JSON structures:
- `assert_json_path_exists("user.address.city")`
- `assert_json_path_value("user.address.city", "London")`

### Status assertions
- `assert_status(expected_status_code)`

---

## 4. Response Wrapper
All HTTP methods return a `ResponseWrapper` object with:

- `.status_code`
- `.json()`
- JSON assertions
- JSON path resolution
- Retry results

Wrapper is intentionally minimal in v1.0.

---

## 5. Simple Mode (Full URL)
Ideal for quick scripts and no-framework testing:

```python
from apitestgenie.simple import get

resp = get("https://example.com/api")
resp.assert_status(200)
