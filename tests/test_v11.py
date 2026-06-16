import datetime
import json as _json
import logging
from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.apitestgenie.client import ApiClient
from src.apitestgenie.simple import get, head, options
from src.apitestgenie.response_wrapper import ResponseWrapper

BASE_URL = "https://jsonplaceholder.typicode.com"


def _make_response(status_code, json_body=None, headers=None, elapsed_seconds=None):
    body = _json.dumps(json_body or {}).encode()
    all_headers = {"content-type": "application/json"}
    if headers:
        all_headers.update(headers)
    resp = httpx.Response(status_code, content=body, headers=all_headers)
    if elapsed_seconds is not None:
        resp.elapsed = datetime.timedelta(seconds=elapsed_seconds)
    return ResponseWrapper(resp)


# ---------------------------------------------------------
# ASSERT_HEADER
# ---------------------------------------------------------

def test_assert_header_passes():
    resp = _make_response(200, {}, headers={"x-custom": "value"})
    resp.assert_header("x-custom")


def test_assert_header_missing():
    resp = _make_response(200, {})
    with pytest.raises(AssertionError, match="x-missing"):
        resp.assert_header("x-missing")


def test_assert_header_case_insensitive():
    resp = _make_response(200, {}, headers={"X-Custom": "value"})
    resp.assert_header("x-custom")


def test_assert_header_chaining():
    resp = _make_response(200, {}, headers={"x-a": "1", "x-b": "2"})
    resp.assert_header("x-a").assert_header("x-b")


# ---------------------------------------------------------
# ASSERT_HEADER_VALUE
# ---------------------------------------------------------

def test_assert_header_value_passes():
    resp = _make_response(200, {}, headers={"content-type": "application/json"})
    resp.assert_header_value("content-type", "application/json")


def test_assert_header_value_wrong_value():
    resp = _make_response(200, {}, headers={"content-type": "application/json"})
    with pytest.raises(AssertionError, match="Expected header 'content-type'"):
        resp.assert_header_value("content-type", "text/html")


def test_assert_header_value_missing_header():
    resp = _make_response(200, {})
    with pytest.raises(AssertionError, match="x-missing"):
        resp.assert_header_value("x-missing", "anything")


def test_assert_header_value_chaining():
    resp = _make_response(200, {}, headers={"x-a": "foo", "x-b": "bar"})
    resp.assert_header_value("x-a", "foo").assert_header_value("x-b", "bar")


# ---------------------------------------------------------
# ASSERT_RESPONSE_TIME
# ---------------------------------------------------------

def test_assert_response_time_passes():
    resp = _make_response(200, {}, elapsed_seconds=0.1)
    resp.assert_response_time(1.0)


def test_assert_response_time_exact_boundary():
    resp = _make_response(200, {}, elapsed_seconds=1.0)
    resp.assert_response_time(1.0)


def test_assert_response_time_fails():
    resp = _make_response(200, {}, elapsed_seconds=2.5)
    with pytest.raises(AssertionError, match="exceeded maximum"):
        resp.assert_response_time(1.0)


def test_assert_response_time_chaining():
    resp = _make_response(200, {"id": 1}, elapsed_seconds=0.05)
    resp.assert_status(200).assert_response_time(1.0).assert_json_key("id")


# ---------------------------------------------------------
# ASSERT_JSON_SCHEMA
# ---------------------------------------------------------

def test_assert_json_schema_passes():
    pytest.importorskip("jsonschema")
    schema = {
        "type": "object",
        "properties": {"id": {"type": "integer"}, "title": {"type": "string"}},
        "required": ["id"],
    }
    resp = _make_response(200, {"id": 1, "title": "foo"})
    resp.assert_json_schema(schema)


def test_assert_json_schema_fails_missing_required():
    pytest.importorskip("jsonschema")
    schema = {"type": "object", "required": ["id"]}
    resp = _make_response(200, {"name": "foo"})
    with pytest.raises(AssertionError, match="JSON schema validation failed"):
        resp.assert_json_schema(schema)


def test_assert_json_schema_fails_wrong_type():
    pytest.importorskip("jsonschema")
    schema = {"type": "object", "properties": {"id": {"type": "integer"}}}
    resp = _make_response(200, {"id": "not-an-int"})
    with pytest.raises(AssertionError, match="JSON schema validation failed"):
        resp.assert_json_schema(schema)


def test_assert_json_schema_no_jsonschema_installed():
    resp = _make_response(200, {"id": 1})
    with patch.dict("sys.modules", {"jsonschema": None}):
        with pytest.raises(ImportError, match="jsonschema"):
            resp.assert_json_schema({})


# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

def _mock_httpx_response(status_code=200):
    resp = httpx.Response(status_code, content=b"{}", headers={"content-type": "application/json"})
    resp.elapsed = datetime.timedelta(seconds=0.1)
    return resp


def test_client_logging_emits(caplog):
    api = ApiClient(BASE_URL, logging=True)
    api.session.request = MagicMock(return_value=_mock_httpx_response())

    with caplog.at_level(logging.INFO, logger="apitestgenie"):
        api.get("/posts/1")

    assert any("GET" in r.message and "200" in r.message for r in caplog.records)


def test_client_logging_disabled_by_default(caplog):
    api = ApiClient(BASE_URL)
    api.session.request = MagicMock(return_value=_mock_httpx_response())

    with caplog.at_level(logging.INFO, logger="apitestgenie"):
        api.get("/posts/1")

    assert len(caplog.records) == 0


def test_simple_logging_emits(caplog):
    with patch("httpx.request", return_value=_mock_httpx_response()):
        with caplog.at_level(logging.INFO, logger="apitestgenie"):
            get(f"{BASE_URL}/posts/1", logging=True)

    assert any("GET" in r.message and "200" in r.message for r in caplog.records)


def test_simple_logging_disabled_by_default(caplog):
    with patch("httpx.request", return_value=_mock_httpx_response()):
        with caplog.at_level(logging.INFO, logger="apitestgenie"):
            get(f"{BASE_URL}/posts/1")

    assert len(caplog.records) == 0


# ---------------------------------------------------------
# RETRY_BACKOFF
# ---------------------------------------------------------

def _make_httpx_response(status_code):
    resp = httpx.Response(status_code, content=b"{}", headers={"content-type": "application/json"})
    return resp


def test_client_retry_backoff_sleep_values():
    api = ApiClient(BASE_URL)
    api.session.request = MagicMock(side_effect=[
        _make_httpx_response(503),
        _make_httpx_response(503),
        _make_httpx_response(200),
    ])

    with patch("time.sleep") as mock_sleep:
        api.get("/posts/1", retries=2, retry_delay=1, retry_on_status=[503], retry_backoff=True)

    # attempt=1 → 1 * 2^1 = 2; attempt=2 → 1 * 2^2 = 4
    calls = [c.args[0] for c in mock_sleep.call_args_list]
    assert calls == [2, 4]


def test_client_no_backoff_uses_fixed_delay():
    api = ApiClient(BASE_URL)
    api.session.request = MagicMock(side_effect=[
        _make_httpx_response(503),
        _make_httpx_response(503),
        _make_httpx_response(200),
    ])

    with patch("time.sleep") as mock_sleep:
        api.get("/posts/1", retries=2, retry_delay=1, retry_on_status=[503], retry_backoff=False)

    calls = [c.args[0] for c in mock_sleep.call_args_list]
    assert calls == [1, 1]


def test_simple_retry_backoff_sleep_values():
    with patch("httpx.request", side_effect=[
        _make_httpx_response(503),
        _make_httpx_response(503),
        _make_httpx_response(200),
    ]):
        with patch("time.sleep") as mock_sleep:
            get(f"{BASE_URL}/posts/1", retries=2, retry_delay=1, retry_on_status=[503], retry_backoff=True)

    calls = [c.args[0] for c in mock_sleep.call_args_list]
    assert calls == [2, 4]


def test_simple_no_backoff_uses_fixed_delay():
    with patch("httpx.request", side_effect=[
        _make_httpx_response(503),
        _make_httpx_response(200),
    ]):
        with patch("time.sleep") as mock_sleep:
            get(f"{BASE_URL}/posts/1", retries=1, retry_delay=1, retry_on_status=[503], retry_backoff=False)

    calls = [c.args[0] for c in mock_sleep.call_args_list]
    assert calls == [1]


# ---------------------------------------------------------
# HEAD — network tests
# ---------------------------------------------------------

def test_client_head():
    api = ApiClient(BASE_URL)
    resp = api.head("/posts/1")
    resp.assert_status(200)


def test_simple_head():
    resp = head(f"{BASE_URL}/posts/1")
    resp.assert_status(200)


# ---------------------------------------------------------
# OPTIONS — network tests
# ---------------------------------------------------------

def test_client_options():
    api = ApiClient(BASE_URL)
    resp = api.options("/posts/1")
    assert resp.status_code in (200, 204)


def test_simple_options():
    resp = options(f"{BASE_URL}/posts/1")
    assert resp.status_code in (200, 204)
