class ResponseWrapper:
    def __init__(self, response):
        self.response = response

    @property
    def status_code(self):
        return self.response.status_code

    def json(self):
        return self.response.json()

    def assert_status(self, expected):
        actual = self.status_code
        if actual != expected:
            raise AssertionError(f"Expected {expected}, got {actual}")
        return self

    def assert_json_key(self, key: str):
        data = self.json()
        if key not in data:
            raise AssertionError(f"Expected key '{key}' not found in JSON response")
        return self

    def assert_json_value(self, key: str, expected_value):
        data = self.json()
        if key not in data:
            raise AssertionError(f"Key '{key}' not found in JSON response")

        actual_value = data[key]
        if actual_value != expected_value:
            raise AssertionError(
                f"Expected '{key}' to be '{expected_value}', got '{actual_value}'"
            )
        return self

    def _resolve_json_path(self, path):
        """Resolve a dotted path like 'user.address.city'."""
        parts = path.split(".")
        current = self.json()

        try:
            for p in parts:
                if isinstance(current, list):
                    p = int(p)  # list index
                current = current[p]
            return current
        except Exception as e:
            raise AssertionError(f"JSON path '{path}' not found: {e}")

    def assert_json_path_exists(self, path):
        _ = self._resolve_json_path(path)
        return self

    def assert_json_path_value(self, path, expected):
        actual = self._resolve_json_path(path)
        if actual != expected:
            raise AssertionError(
                f"JSON path '{path}' expected '{expected}', got '{actual}'"
            )
        return self
