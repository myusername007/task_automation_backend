from fastapi import status

def test_register_and_login(client):

    # Test user registration
    register_response = client.post(
        "/auth/register",
        json = {
            "email": "test@example.com",
            "password": "12345678"
        }
    )

    assert register_response.status_code == status.HTTP_201_CREATED

    #Test user login
    login_response = client.post(
        "/auth/login",
        data = {
            "username": "test@example.com",
            "password": "12345678"
        }
    )

    assert login_response.status_code == status.HTTP_200_OK

    token = login_response.json()["access_token"]
    assert token is not None

    #access protected endpoint
    me_response = client.get(
        "/users/me",
        headers = {
            "Authorization": f"Bearer {token}"
        }
    )

    assert me_response.status_code == status.HTTP_200_OK
    assert me_response.json()["email"] == "test@example.com"

    #test login with wrong credentials
    wrong_login_response = client.post(
        "/auth/login",
        data = {
            "username": "wrong@example.com",
            "password": "wrongpassword"
        }
    )

    assert wrong_login_response.status_code == status.HTTP_401_UNAUTHORIZED