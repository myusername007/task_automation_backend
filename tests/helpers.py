from fastapi import status

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

