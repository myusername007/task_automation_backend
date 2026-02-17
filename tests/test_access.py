from fastapi import status

#test 1
def test_userA_cannot_access_userB_tasks(client):
    #Register user A
    register_response_A = client.post(
        "/auth/register",
        json = {
            "email": "userA@example.com",
            "password": "passwordA"
        }
    )
    assert register_response_A.status_code == status.HTTP_201_CREATED

    #login user A
    login_response_A = client.post(
        "/auth/login",
        data = {
            "username": "userA@example.com",
            "password": "passwordA"
        }
    )
    assert login_response_A.status_code == status.HTTP_200_OK
    token_A = login_response_A.json()["access_token"]
    assert token_A is not None

    #Register user B
    register_response_B = client.post(
        "/auth/register",
        json = {
            "email": "userB@example.com",
            "password": "passwordB"
        }
    )
    assert register_response_B.status_code == status.HTTP_201_CREATED

    #login user B
    login_response_B = client.post(
        "/auth/login",
        data = {
            "username": "userB@example.com",
            "password": "passwordB"
        }
    )
    assert login_response_B.status_code == status.HTTP_200_OK
    token_B = login_response_B.json()["access_token"]
    assert token_B is not None
    
    #user B creates a task
    create_task_response_B = client.post(
        "/tasks",
        json = {
            "title": "User B Task",
            "description": "Task User B"
        },
        headers = {
            "Authorization": f"Bearer {token_B}"

        }
    )
    assert create_task_response_B.status_code == status.HTTP_201_CREATED
    task_id_B = create_task_response_B.json()["id"]

    #user A tries to access user B task
    access_task_response_A = client.get(
        f"/tasks/{task_id_B}",
        headers = {
            "Authorization": f"Bearer {token_A}"
        }
    )
    assert access_task_response_A.status_code == status.HTTP_404_NOT_FOUND





#test 2
def test_userA_cannot_access_userB_taskrun(client):
    #Register user A
    register_response_A = client.post(
        "/auth/register",
        json = {
            "email": "userA@example.com",
            "password": "passwordA"
        }
    )
    assert register_response_A.status_code == status.HTTP_201_CREATED

    #login user A
    login_response_A = client.post(
        "/auth/login",
        data = {
            "username": "userA@example.com",
            "password": "passwordA"
        }
    )
    assert login_response_A.status_code == status.HTTP_200_OK
    token_A = login_response_A.json()["access_token"]
    assert token_A is not None

    #Register user B
    register_response_B = client.post(
        "/auth/register",
        json = {
            "email": "userB@example.com",
            "password": "passwordB"
        }
    )
    assert register_response_B.status_code == status.HTTP_201_CREATED

    #login user B
    login_response_B = client.post(
        "/auth/login",
        data = {
            "username": "userB@example.com",
            "password": "passwordB"
        }
    )
    assert login_response_B.status_code == status.HTTP_200_OK
    token_B = login_response_B.json()["access_token"]
    assert token_B is not None
    
    #user B creates a task
    create_task_response_B = client.post(
        "/tasks",
        json = {
            "title": "User B Task",
            "description": "Task User B"
        },
        headers = {
            "Authorization": f"Bearer {token_B}"

        }
    )
    assert create_task_response_B.status_code == status.HTTP_201_CREATED
    task_id_B = create_task_response_B.json()["id"]

    #User A tries to run user B task
    runtask_response_B = client.post(
        f"/tasks/{task_id_B}/start",
        data = {
            "task_id": task_id_B
        },
        headers = {
            "Authorization": f"Bearer {token_A}"
        }

    )
    assert runtask_response_B.status_code == status.HTTP_404_NOT_FOUND





#test 3
def test_userA_cannot_access_userB_taskrun_and_run(client):
    #Register user A
    register_response_A = client.post(
        "/auth/register",
        json = {
            "email": "userA@example.com",
            "password": "passwordA"
        }
    )
    assert register_response_A.status_code == status.HTTP_201_CREATED

    #login user A
    login_response_A = client.post(
        "/auth/login",
        data = {
            "username": "userA@example.com",
            "password": "passwordA"
        }
    )
    assert login_response_A.status_code == status.HTTP_200_OK
    token_A = login_response_A.json()["access_token"]
    assert token_A is not None

    #Register user B
    register_response_B = client.post(
        "/auth/register",
        json = {
            "email": "userB@example.com",
            "password": "passwordB"
        }
    )
    assert register_response_B.status_code == status.HTTP_201_CREATED

    #login user B
    login_response_B = client.post(
        "/auth/login",
        data = {
            "username": "userB@example.com",
            "password": "passwordB"
        }
    )
    assert login_response_B.status_code == status.HTTP_200_OK
    token_B = login_response_B.json()["access_token"]
    assert token_B is not None
    
    #user B creates a task
    create_task_response_B = client.post(
        "/tasks",
        json = {
            "title": "User B Task",
            "description": "Task User B"
        },
        headers = {
            "Authorization": f"Bearer {token_B}"

        }
    )
    assert create_task_response_B.status_code == status.HTTP_201_CREATED
    task_id_B = create_task_response_B.json()["id"]

    #User B runs the task
    runtask_response_B = client.post(
        f"/tasks/{task_id_B}/start",
        data = {
            "task_id": task_id_B
        },
        headers = {
            "Authorization": f"Bearer {token_B}"
        }

    )
    assert runtask_response_B.status_code == status.HTTP_200_OK

    #User A tries to access user B task runs
    access_taskruns_response_A = client.get(
        f"/tasks/{task_id_B}/runs",
        headers = {
            "Authorization": f"Bearer {token_A}"
        }
    )
    assert access_taskruns_response_A.status_code == status.HTTP_404_NOT_FOUND


    



    