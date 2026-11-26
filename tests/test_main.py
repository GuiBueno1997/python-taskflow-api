
def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to TaskFlow API!",
        "status": "online"
    }


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_get_task_not_found(client):
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_create_task(client):
    task_data = {
        "title": "Learn automated testing",
        "description": "Testing POST endpoint with Pytest",
        "completed": False
    }

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["completed"] is False


def test_get_task(client):
    task_data = {
        "title": "Practice GET endpoint",
        "description": "Testing task retrieval",
        "completed": False
    }

    create_response = client.post("/tasks", json=task_data)

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["completed"] is False


def test_update_task(client):
    original_task = {
        "title": "Original task",
        "description": "Original description",
        "completed": False
    }

    create_response = client.post("/tasks", json=original_task)
    task_id = create_response.json()["id"]

    updated_task = {
        "title": "Updated task",
        "description": "Updated description",
        "completed": True
    }

    response = client.put(
        f"/tasks/{task_id}",
        json=updated_task
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Updated task"
    assert data["description"] == "Updated description"
    assert data["completed"] is True


def test_partial_update_task(client):
    original_task = {
        "title": "Original task",
        "description": "Original description",
        "completed": False
    }

    create_response = client.post("/tasks", json=original_task)
    task_id = create_response.json()["id"]

    update_data = {
        "completed": True
    }

    response = client.patch(
        f"/tasks/{task_id}",
        json=update_data
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == original_task["title"]
    assert data["description"] == original_task["description"]
    assert data["completed"] is True


def test_delete_task(client):
    task_data = {
        "title": "Task to delete",
        "description": "Testing DELETE endpoint",
        "completed": False
    }

    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Task deleted successfully!"
    }

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Task not found"
    }


def test_list_tasks_filter_completed(client):
    tasks = [
        {
            "title": "Completed task",
            "description": "This task is completed",
            "completed": True
        },
        {
            "title": "Pending task",
            "description": "This task is pending",
            "completed": False
        },
        {
            "title": "Another completed task",
            "description": "This task is also completed",
            "completed": True
        }
    ]

    for task in tasks:
        client.post("/tasks", json=task)

    response = client.get("/tasks?completed=true")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    for task in data:
        assert task["completed"] is True


def test_list_tasks_limit(client):
    for number in range(5):
        task_data = {
            "title": f"Task {number}",
            "description": "Testing pagination limit",
            "completed": False
        }

        client.post("/tasks", json=task_data)

    response = client.get("/tasks?limit=3")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3


def test_create_task_without_title(client):
    task_data = {
        "description": "Testing missing required field",
        "completed": False
    }

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 422



def test_create_task_without_completed(client):
    task_data = {
        "title": "Testing missing completed field",
        "description": "Testing validation"
    }

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 422


def test_list_tasks_invalid_limit_zero(client):
    response = client.get("/tasks?limit=0")

    assert response.status_code == 422


def test_list_tasks_invalid_limit_above_maximum(client):
    response = client.get("/tasks?limit=101")

    assert response.status_code == 422


def test_update_nonexistent_task(client):
    task_data = {
        "title": "Updated task",
        "description": "Testing missing task",
        "completed": False
    }

    response = client.put("/tasks/999999", json=task_data)

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_partial_update_nonexistent_task(client):
    update_data = {
        "completed": True
    }

    response = client.patch("/tasks/999999", json=update_data)

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_get_subtasks(client):
    response = client.get(
        "/tasks/10/subtasks?completed=true&limit=5"
    )

    assert response.status_code == 200
    assert response.json() == {
        "task_id": 10,
        "completed": True,
        "limit": 5
    }


def test_get_specific_subtask(client):
    response = client.get("/tasks/10/subtasks/25")

    assert response.status_code == 200
    assert response.json() == {
        "task_id": 10,
        "subtask_id": 25,
        "message": "Subtask 25 for task 10 requested"
    }
