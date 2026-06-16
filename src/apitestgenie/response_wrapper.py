from typing import Any, Self

import httpx


class ResponseWrapper:
    def __init__(self, response: httpx.Response) -> None:
        self.response = response

    @property
    def status_code(self) -> int:
        return self.response.status_code

    def json(self) -> Any:
        return self.response.json()

    def assert_status(self, expected: int) -> Self:
        actual = self.status_code
        if actual != expected:
            context = ""
            try:
                method = self.response.request.method
                url = str(self.response.request.url)
                context += f"\n  {method} {url}"
            except RuntimeError:
                pass
            try:
                body = self.response.text[:200]
                if body:
                    context += f"\n  Response: {body}"
            except Exception:
                pass
            raise AssertionError(f"Expected status {expected}, got {actual}{context}")
        return self

    def assert_header(self, name: str) -> Self:
        if name.lower() not in self.response.headers:
            available = list(self.response.headers.keys())
            raise AssertionError(
                f"Header '{name}' not found in response. Available headers: {available}"
            )
        return self

    def assert_header_value(self, name: str, expected: str) -> Self:
        actual = self.response.headers.get(name)
        if actual is None:
            available = list(self.response.headers.keys())
            raise AssertionError(
                f"Header '{name}' not found in response. Available headers: {available}"
            )
        if actual != expected:
            raise AssertionError(
                f"Expected header '{name}' to be {expected!r}, got {actual!r}"
            )
        return self

    def assert_response_time(self, max_seconds: int | float) -> Self:
        elapsed = self.response.elapsed.total_seconds()
        if elapsed > max_seconds:
            raise AssertionError(
                f"Response time {elapsed:.3f}s exceeded maximum {max_seconds}s"
            )
        return self

    def assert_json_key(self, key: str) -> Self:
        data = self.json()
        if not isinstance(data, dict):
            raise AssertionError(
                f"Expected a JSON object to check key '{key}', but got {type(data).__name__}"
            )
        if key not in data:
            available = list(data.keys())
            raise AssertionError(
                f"Key '{key}' not found in JSON response. Available keys: {available}"
            )
        return self

    def assert_json_value(self, key: str, expected_value: Any) -> Self:
        data = self.json()
        if not isinstance(data, dict):
            raise AssertionError(
                f"Expected a JSON object to check key '{key}', but got {type(data).__name__}"
            )
        if key not in data:
            available = list(data.keys())
            raise AssertionError(
                f"Key '{key}' not found in JSON response. Available keys: {available}"
            )

        actual_value = data[key]
        if actual_value != expected_value:
            type_hint = ""
            if type(actual_value) is not type(expected_value):
                type_hint = (
                    f" (type mismatch: expected {type(expected_value).__name__},"
                    f" got {type(actual_value).__name__})"
                )
            raise AssertionError(
                f"Expected '{key}' to be {expected_value!r}, got {actual_value!r}{type_hint}"
            )
        return self

    def _resolve_json_path(self, path: str) -> Any:
        """Resolve a dotted path like 'user.address.city'."""
        parts = path.split(".")
        current = self.json()

        try:
            for p in parts:
                if isinstance(current, list):
                    try:
                        p = int(p)
                    except ValueError:
                        raise AssertionError(
                            f"JSON path '{path}' is invalid: '{p}' is not a valid list index"
                        )
                current = current[p]
            return current
        except KeyError:
            raise AssertionError(f"JSON path '{path}' not found: key '{p}' does not exist")
        except IndexError:
            raise AssertionError(f"JSON path '{path}' not found: list index '{p}' is out of range")
        except TypeError:
            raise AssertionError(
                f"JSON path '{path}' not found: cannot index into {type(current).__name__} with '{p}'"
            )

    def assert_json_path_exists(self, path: str) -> Self:
        _ = self._resolve_json_path(path)
        return self

    def assert_json_path_value(self, path: str, expected: Any) -> Self:
        actual = self._resolve_json_path(path)
        if actual != expected:
            type_hint = ""
            if type(actual) is not type(expected):
                type_hint = (
                    f" (type mismatch: expected {type(expected).__name__},"
                    f" got {type(actual).__name__})"
                )
            raise AssertionError(
                f"JSON path '{path}': expected {expected!r}, got {actual!r}{type_hint}"
            )
        return self

    def assert_json_schema(self, schema: dict) -> Self:
        try:
            import jsonschema
        except ImportError:
            raise ImportError(
                "jsonschema is required for assert_json_schema. "
                "Install it with: pip install jsonschema"
            )
        data = self.json()
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.ValidationError as e:
            raise AssertionError(f"JSON schema validation failed: {e.message}")
        return self
