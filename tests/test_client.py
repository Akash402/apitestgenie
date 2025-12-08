from apitestgenie.client import ApiClient
from apitestgenie.simple import get

def test_client_mode_get():
    api = ApiClient("https://jsonplaceholder.typicode.com")
    response = api.get("/posts/1")

    response.assert_status(200)
    response.assert_json_key("id")
    response.assert_json_value("id", 1)


def test_simple_mode_get():
    response = get("https://jsonplaceholder.typicode.com/posts/1")

    response.assert_status(200)
    response.assert_json_key("id")
    response.assert_json_value("id", 1)
