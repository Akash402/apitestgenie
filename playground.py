import logging

from src.apitestgenie.client import ApiClient
from src.apitestgenie.simple import get, post, put, patch, delete, head, options

logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")

BASE_URL = "https://jsonplaceholder.typicode.com"


def section(title):
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print('=' * 50)


def main():

    # --------------------------------------------------
    # V1.0 FEATURES
    # --------------------------------------------------

    section("CLIENT MODE — CRUD")
    api = ApiClient(BASE_URL, headers={"X-Demo": "123"}, timeout=5)

    resp = api.get("/posts/1")
    print("GET status:", resp.status_code)
    print("GET json:", resp.json())

    resp = api.post("/posts", json={"title": "foo"})
    print("POST status:", resp.status_code)
    print("POST json:", resp.json())

    resp = api.put("/posts/1", json={"id": 1, "title": "updated"})
    print("PUT status:", resp.status_code)

    resp = api.patch("/posts/1", json={"title": "patched"})
    print("PATCH status:", resp.status_code)

    resp = api.delete("/posts/1")
    print("DELETE status:", resp.status_code)

    section("SIMPLE MODE — CRUD")
    print("Simple GET:", get(f"{BASE_URL}/posts/1").json())
    print("Simple POST:", post(f"{BASE_URL}/posts", json={"hello": "world"}).json())
    print("Simple PUT:", put(f"{BASE_URL}/posts/1", json={"id": 1}).json())
    print("Simple PATCH:", patch(f"{BASE_URL}/posts/1", json={"name": "patched"}).json())
    print("Simple DELETE status:", delete(f"{BASE_URL}/posts/1").status_code)

    # --------------------------------------------------
    # V1.1 — HEAD & OPTIONS
    # --------------------------------------------------

    section("HEAD & OPTIONS")
    resp = api.head("/posts/1")
    print("Client HEAD status:", resp.status_code)

    resp = api.options("/posts/1")
    print("Client OPTIONS status:", resp.status_code)

    resp = head(f"{BASE_URL}/posts/1")
    print("Simple HEAD status:", resp.status_code)

    resp = options(f"{BASE_URL}/posts/1")
    print("Simple OPTIONS status:", resp.status_code)

    # --------------------------------------------------
    # V1.1 — HEADER ASSERTIONS
    # --------------------------------------------------

    section("HEADER ASSERTIONS")
    resp = api.get("/posts/1")

    resp.assert_header("content-type")
    print("assert_header('content-type') passed")

    resp.assert_header_value("content-type", "application/json; charset=utf-8")
    print("assert_header_value passed")

    try:
        resp.assert_header("x-does-not-exist")
    except AssertionError as e:
        print("assert_header (missing) correctly raised:", e)

    try:
        resp.assert_header_value("content-type", "text/html")
    except AssertionError as e:
        print("assert_header_value (wrong value) correctly raised:", e)

    # --------------------------------------------------
    # V1.1 — RESPONSE TIME ASSERTION
    # --------------------------------------------------

    section("RESPONSE TIME ASSERTION")
    resp = api.get("/posts/1")

    resp.assert_response_time(5.0)
    print(f"assert_response_time(5.0) passed — elapsed: {resp.response.elapsed.total_seconds():.3f}s")

    try:
        resp.assert_response_time(0.00001)
    except AssertionError as e:
        print("assert_response_time (too slow) correctly raised:", e)

    # --------------------------------------------------
    # V1.1 — JSON SCHEMA VALIDATION
    # --------------------------------------------------

    section("JSON SCHEMA VALIDATION")
    try:
        import jsonschema  # noqa: F401

        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "body": {"type": "string"},
                "userId": {"type": "integer"},
            },
            "required": ["id", "title", "body", "userId"],
        }

        resp = api.get("/posts/1")
        resp.assert_json_schema(schema)
        print("assert_json_schema passed")

        bad_schema = {"type": "object", "required": ["nonexistent_field"]}
        try:
            resp.assert_json_schema(bad_schema)
        except AssertionError as e:
            print("assert_json_schema (invalid) correctly raised:", e)

    except ImportError:
        print("jsonschema not installed — skipping. Run: pip install jsonschema")

    # --------------------------------------------------
    # V1.1 — LOGGING
    # --------------------------------------------------

    section("LOGGING (watch for apitestgenie: INFO lines)")
    api_with_log = ApiClient(BASE_URL, logging=True)
    api_with_log.get("/posts/1")
    api_with_log.post("/posts", json={"title": "log test"})

    print("\nSimple mode logging:")
    get(f"{BASE_URL}/posts/2", logging=True)

    # --------------------------------------------------
    # V1.1 — EXPONENTIAL BACKOFF
    # --------------------------------------------------

    section("EXPONENTIAL BACKOFF (simulated — no real retries hit)")
    # retry_on_status=[999] will never match, so no actual sleep occurs,
    # but this confirms the param is accepted without error.
    resp = api.get("/posts/1", retries=3, retry_delay=1, retry_on_status=[999], retry_backoff=True)
    print("retry_backoff=True accepted, status:", resp.status_code)

    # --------------------------------------------------
    # CHAINING — all v1.1 assertions together
    # --------------------------------------------------

    section("CHAINING ALL ASSERTIONS")
    api.get("/posts/1") \
        .assert_status(200) \
        .assert_response_time(5.0) \
        .assert_header("content-type") \
        .assert_json_key("id") \
        .assert_json_value("id", 1)
    print("Full chain passed")

    print("\nAll playground checks complete.")


if __name__ == "__main__":
    main()
