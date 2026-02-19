from fastapi import status
import time

def register(client, email: str, password: str) -> dict:
    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code == status.HTTP_201_CREATED
    return r.json()

def login_get_token(client, email: str, password: str) -> str:
    r = client.post("/auth/login", data={"username":email, "password": password})
    assert r.status_code == status.HTTP_200_OK
    return r.json()["access_token"]

def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

def create_task(client, token: str, title: str, description: str) -> dict:
    r = client.post("/tasks", json={"title": title, "description": description}, headers = auth_headers(token))
    assert r.status_code == status.HTTP_201_CREATED
    return r.json()

def wait_for_task(client, token: str, task_id: int, expected: str, timeout_sec: float):
    start = time.time()
    while time.time() - start < timeout_sec:
        r = client.get(f"/tasks/{task_id}", headers = auth_headers(token))
        if r.status_code == 200:
            if r.json()["status"] == expected:
                return r.json()
            time.sleep(0.1)
    raise AssertionError(f"Task {task_id} did not reach status={expected} within {timeout_sec}s")
    