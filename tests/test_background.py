from fastapi import status
from tests.helpers import register, login_get_token, auth_headers, wait_for_task, create_task


def test_start_creates_run_and_sets_pending_or_running(client):
    
    #Register user
    register(client, "test1@example.com", "1234")
    #login user
    token = login_get_token(client, "test1@example.com", "1234")
    assert token is not None
    #create task
    task = create_task(client, token, "Task1", "Desc1")
    task_id = task["id"]

    #start task
    start_response = client.post(f"/tasks/{task_id}/start", headers=auth_headers(token))
    assert start_response.status_code == status.HTTP_200_OK

    #wait for task to be done
    task_result = wait_for_task(client, token, task_id, expected="running", timeout_sec=3.0)
    assert task_result["status"] == "running"
    
    #check runs returns the run
    runs_response = client.get(f"/tasks/{task_id}/runs", headers=auth_headers(token))
    assert runs_response.status_code == status.HTTP_200_OK
    assert len(runs_response.json()) >= 1



def test_task_eventually_becomes_done_and_has_result(client):
    #Register user
    register(client, "test1@example.com", "1234")
    #login user
    token = login_get_token(client, "test1@example.com", "1234")
    assert token is not None
    #create task
    task = create_task(client, token, "Task1", "Desc1")
    task_id = task["id"]

    #start task
    start_response = client.post(f"/tasks/{task_id}/start", headers=auth_headers(token))
    assert start_response.status_code == status.HTTP_200_OK

    #wait for task to be done
    task_result = wait_for_task(client, token, task_id, expected="done", timeout_sec=5.0)
    assert task_result is not None
    assert task_result["status"] == "done"
    
    #check runs returns the run
    runs_response = client.get(f"/tasks/{task_id}/runs", headers=auth_headers(token))
    assert runs_response.status_code == status.HTTP_200_OK
    assert len(runs_response.json()) >= 1

