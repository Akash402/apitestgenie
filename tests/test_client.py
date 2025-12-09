from src.apitestgenie.client import ApiClient
from src.apitestgenie.simple import get, post, put, patch, delete

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
