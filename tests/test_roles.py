from fastapi import status
from app.db.models import User

def test_user_cannot_access_admin_tasks(client): #Тест: user не може отримати /admin/tasks

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
    admin_tasks_access_response = client.get(
        "/admin/tasks",
        headers = {
            "Authorization": f"Bearer {token}"
        }
    )

    assert admin_tasks_access_response.status_code == status.HTTP_403_FORBIDDEN




def test_admin_can_access_admin_tasks(client, db):
    admin_user = client.post(
        "/auth/register",
        json = {
            "email": "admin@example.com",
            "password": "adminpassword"
        }
    )
    assert admin_user.status_code == status.HTTP_201_CREATED
    admin_id = admin_user.json()["id"]
    user = db.query(User).filter(User.id == admin_id).first()
    assert user is not None
    user.is_admin = True
    db.commit()

    login_response = client.post(
        "/auth/login",
        data = {
            "username": "admin@example.com",
            "password": "adminpassword"
        }
    )

    assert login_response.status_code == status.HTTP_200_OK

    token = login_response.json()["access_token"]
    assert token is not None

    admin_access_response = client.get(
        "/admin/tasks",
        headers = {
            "Authorization": f"Bearer {token}"
        }
    )

    assert admin_access_response.status_code == status.HTTP_200_OK