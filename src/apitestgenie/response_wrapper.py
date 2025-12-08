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
