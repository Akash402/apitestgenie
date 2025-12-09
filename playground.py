from src.apitestgenie.client import ApiClient
from src.apitestgenie.simple import get, post, put, patch, delete

def main():
    base_url = "https://jsonplaceholder.typicode.com"

    print("=== CLIENT MODE TESTS ===")
    api = ApiClient(base_url, headers={"X-Demo": "123"}, timeout=5)

    # GET
    resp = api.get("/posts/1")
    print("GET status:", resp.status_code)
    print("GET json:", resp.json())

    # POST
    resp_post = api.post("/posts", json={"title": "foo"})
    print("POST status:", resp_post.status_code)
    print("POST json:", resp_post.json())

    # PUT
    resp_put = api.put("/posts/1", json={"id": 1, "title": "updated"})
    print("PUT status:", resp_put.status_code)
    print("PUT json:", resp_put.json())

    # PATCH
    resp_patch = api.patch("/posts/1", json={"title": "patched"})
    print("PATCH status:", resp_patch.status_code)
    print("PATCH json:", resp_patch.json())

    # DELETE
    resp_delete = api.delete("/posts/1")
    print("DELETE status:", resp_delete.status_code)


    print("\n=== SIMPLE MODE TESTS ===")

    # Simple GET
    s_get = get(f"{base_url}/posts/1")
    print("Simple GET:", s_get.json())

    # Simple POST
    s_post = post(f"{base_url}/posts", json={"hello": "world"})
    print("Simple POST:", s_post.json())

    # Simple PUT
    s_put = put(f"{base_url}/posts/1", json={"id": 1, "new": "data"})
    print("Simple PUT:", s_put.json())

    # Simple PATCH
    s_patch = patch(f"{base_url}/posts/1", json={"name": "patched"})
    print("Simple PATCH:", s_patch.json())

    # Simple DELETE
    s_delete = delete(f"{base_url}/posts/1")
    print("Simple DELETE status:", s_delete.status_code)

if __name__ == "__main__":
    main()
