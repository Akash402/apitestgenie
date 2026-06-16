import httpx
import pytest
from src.apitestgenie.client import ApiClient
from src.apitestgenie.simple import get, post, put, patch, delete
from src.apitestgenie.response_wrapper import ResponseWrapper

BASE_URL = "https://jsonplaceholder.typicode.com"

# ---------------------------------------------------------
# GET TESTS
# ---------------------------------------------------------

def test_client_get():
    api = ApiClient(BASE_URL)
    resp = api.get("/posts/1")
    resp.assert_status(200)
    resp.assert_json_key("id")
    resp.assert_json_value("id", 1)

def test_simple_get():
    resp = get(f"{BASE_URL}/posts/1")
    resp.assert_status(200)
    resp.assert_json_key("id")
    resp.assert_json_value("id", 1)

# ---------------------------------------------------------
# POST TESTS
# ---------------------------------------------------------

def test_client_post():
    api = ApiClient(BASE_URL)
    resp = api.post("/posts", json={"title": "foo", "body": "bar", "userId": 1})
    resp.assert_status(201)
    resp.assert_json_key("id")

def test_simple_post():
    resp = post(f"{BASE_URL}/posts", json={"title": "foo"})
    resp.assert_status(201)
    resp.assert_json_key("id")


# ---------------------------------------------------------
# PUT TESTS
# ---------------------------------------------------------

def test_client_put():
    api = ApiClient(BASE_URL)
    resp = api.put("/posts/1", json={"id": 1, "title": "updated"})
    resp.assert_status(200)
    resp.assert_json_key("id")
    resp.assert_json_value("id", 1)

def test_simple_put():
    resp = put(f"{BASE_URL}/posts/1", json={"id": 1, "title": "updated"})
    resp.assert_status(200)
    resp.assert_json_key("id")
    resp.assert_json_value("id", 1)

# ---------------------------------------------------------
# PATCH TESTS
# ---------------------------------------------------------

def test_client_patch():
    api = ApiClient(BASE_URL)
    resp = api.patch("/posts/1", json={"title": "patched"})
    resp.assert_status(200)
    resp.assert_json_key("id")
    resp.assert_json_value("id", 1)

def test_simple_patch():
    resp = patch(f"{BASE_URL}/posts/1", json={"title": "patched"})
    resp.assert_status(200)
    resp.assert_json_key("id")
    resp.assert_json_value("id", 1)

# ---------------------------------------------------------
# DELETE TESTS
# ---------------------------------------------------------

def test_client_delete():
    api = ApiClient(BASE_URL)
    resp = api.delete("/posts/1")
    resp.assert_status(200)

def test_simple_delete():
    resp = delete(f"{BASE_URL}/posts/1")
    resp.assert_status(200)

# ---------------------------------------------------------
# SIMPLE MODE TIMEOUT TESTS
# ---------------------------------------------------------

def test_simple_mode_timeout():
    resp = get(f"{BASE_URL}/posts/1", timeout=5)
    resp.assert_status(200)


# ---------------------------------------------------------
# OFFLINE UNIT TESTS (no network required)
# ---------------------------------------------------------

def _make_mock_response(status_code, json_body):
    """Build a ResponseWrapper from a mock httpx response."""
    import json as _json
    body = _json.dumps(json_body).encode()
    mock = httpx.Response(status_code, content=body, headers={"content-type": "application/json"})
    return ResponseWrapper(mock)


def test_assert_status_passes():
    resp = _make_mock_response(200, {"id": 1})
    resp.assert_status(200)


def test_assert_status_fails():
    resp = _make_mock_response(404, {"error": "not found"})
    with pytest.raises(AssertionError, match="Expected status 200, got 404"):
        resp.assert_status(200)


def test_assert_json_key_passes():
    resp = _make_mock_response(200, {"id": 1, "title": "foo"})
    resp.assert_json_key("id")
    resp.assert_json_key("title")


def test_assert_json_key_missing():
    resp = _make_mock_response(200, {"id": 1})
    with pytest.raises(AssertionError, match="not found"):
        resp.assert_json_key("missing")


def test_assert_json_key_on_list_response():
    resp = _make_mock_response(200, [{"id": 1}, {"id": 2}])
    with pytest.raises(AssertionError, match="Expected a JSON object"):
        resp.assert_json_key("id")


def test_assert_json_value_passes():
    resp = _make_mock_response(200, {"id": 42})
    resp.assert_json_value("id", 42)


def test_assert_json_value_fails():
    resp = _make_mock_response(200, {"id": 42})
    with pytest.raises(AssertionError, match="Expected 'id' to be 1, got 42"):
        resp.assert_json_value("id", 1)


def test_assert_json_path_exists():
    resp = _make_mock_response(200, {"user": {"address": {"city": "London"}}})
    resp.assert_json_path_exists("user.address.city")


def test_assert_json_path_value():
    resp = _make_mock_response(200, {"user": {"address": {"city": "London"}}})
    resp.assert_json_path_value("user.address.city", "London")


def test_assert_json_path_missing():
    resp = _make_mock_response(200, {"user": {}})
    with pytest.raises(AssertionError, match="not found"):
        resp.assert_json_path_exists("user.address.city")


def test_chained_assertions():
    resp = _make_mock_response(200, {"id": 1, "title": "foo"})
    resp.assert_status(200).assert_json_key("id").assert_json_value("id", 1)


def test_api_client_context_manager():
    with ApiClient("https://example.com") as api:
        assert api is not None


def test_response_wrapper_status_code():
    resp = _make_mock_response(201, {})
    assert resp.status_code == 201


def test_response_wrapper_json():
    resp = _make_mock_response(200, {"key": "value"})
    assert resp.json() == {"key": "value"}
