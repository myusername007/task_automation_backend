from fastapi import status
from tests.helpers import register, login_get_token, auth_headers

#test 1
def test_userA_cannot_access_userB_tasks(client):
    #Register user A
    register(client, "userA@example.com", "passwordA")

    #login user A
    token_A = login_get_token(client, "userA@example.com", "passwordA")
    assert token_A is not None

    #Register user B
    register(client, "userB@example.com", "passwordB")

    #login user B
    token_B = login_get_token(client, "userB@example.com", "passwordB")
    assert token_B is not None
    
    #user B creates a task
    create_task_response_B = client.post(
        "/tasks",
        json = {
            "title": "User B Task",
            "description": "Task User B"
        },
        headers = auth_headers(token_B)
    )
    assert create_task_response_B.status_code == status.HTTP_201_CREATED
    task_id_B = create_task_response_B.json()["id"]

    #user A tries to access user B task
    access_task_response_A = client.get(
        f"/tasks/{task_id_B}",
        headers = auth_headers(token_A)
    )
    assert access_task_response_A.status_code == status.HTTP_404_NOT_FOUND





#test 2
def test_userA_cannot_access_userB_taskrun(client):
    #Register user A
    register(client, "userA@example.com", "passwordA")

    #login user A
    token_A = login_get_token(client, "userA@example.com", "passwordA")
    assert token_A is not None

    #Register user B
    register(client, "userB@example.com", "passwordB")

    #login user B
    token_B = login_get_token(client, "userB@example.com", "passwordB")
    assert token_B is not None
    
    #user B creates a task
    create_task_response_B = client.post(
        "/tasks",
        json = {
            "title": "User B Task",
            "description": "Task User B"
        },
        headers = auth_headers(token_B)
    )
    assert create_task_response_B.status_code == status.HTTP_201_CREATED
    task_id_B = create_task_response_B.json()["id"]

    #User A tries to run user B task
    runtask_response_B = client.post(
        f"/tasks/{task_id_B}/start",
        headers = auth_headers(token_A)

    )
    assert runtask_response_B.status_code == status.HTTP_404_NOT_FOUND





#test 3
def test_userA_cannot_access_userB_taskrun_and_run(client):
    #Register user A
    register(client, "userA@example.com", "passwordA")

    #login user A
    token_A = login_get_token(client, "userA@example.com", "passwordA")
    assert token_A is not None

    #Register user B
    register(client, "userB@example.com", "passwordB")

    #login user B
    token_B = login_get_token(client, "userB@example.com", "passwordB")
    assert token_B is not None
    
    #user B creates a task
    create_task_response_B = client.post(
        "/tasks",
        json = {
            "title": "User B Task",
            "description": "Task User B"
        },
        headers = auth_headers(token_B)
    )
    assert create_task_response_B.status_code == status.HTTP_201_CREATED
    task_id_B = create_task_response_B.json()["id"]

    #User B runs the task
    runtask_response_B = client.post(
        f"/tasks/{task_id_B}/start",
        headers = auth_headers(token_B)

    )
    assert runtask_response_B.status_code == status.HTTP_200_OK

    #User A tries to access user B task runs
    access_taskruns_response_A = client.get(
        f"/tasks/{task_id_B}/runs",
        headers = auth_headers(token_A)
    )
    assert access_taskruns_response_A.status_code == status.HTTP_404_NOT_FOUND


    



    