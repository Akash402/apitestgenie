from src.apitestgenie.client import ApiClient
from src.apitestgenie.simple import get

def main():
    print("=== Testing Client Mode ===")
    api = ApiClient("https://jsonplaceholder.typicode.com")
    resp = api.get("/posts/1")
    print("Status:", resp.status_code)
    print("JSON:", resp.json())
    resp.assert_status(200)
    resp.assert_json_key("id")
    resp.assert_json_value("id", 1)
    print("Client mode tests passed!\n")

    print("=== Testing Simple Mode ===")
    resp2 = get("https://jsonplaceholder.typicode.com/posts/1")
    print("Status:", resp2.status_code)
    print("JSON:", resp2.json())
    resp2.assert_status(200)
    resp2.assert_json_key("id")
    resp2.assert_json_value("id", 1)
    print("Simple mode tests passed!\n")


if __name__ == "__main__":
    main()
