
from fastapi import FastAPI, Query

# Creating our API application
app = FastAPI(
    title="TaskFlow API",
    description="A RESTful Task Management API built with Python",
    version="1.0.0"
)


# First endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to TaskFlow API!",
        "status": "online"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

# Path Parameters
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {
        "task_id": task_id,
        "message": f"Task {task_id} requested"
    }


# Query Parameters
@app.get("/tasks")
def list_tasks(completed: bool | None = None, limit: int = 10):
    return {
        "completed": completed,
        "limit": limit
    }

# Task endpoints

# Get subtasks from a specific task
@app.get("/tasks/{task_id}/subtasks")
def get_subtasks(
    task_id: int, 
    completed: bool | None = None, 
    limit: int = Query(default=10, gt=0, le=100)
):
    return {
        "task_id": task_id,
        "completed": completed,
        "limit": limit
    }


# Get a specific subtask from a task
@app.get("/tasks/{task_id}/subtasks/{subtask_id}")
def get_subtask(task_id: int, subtask_id: int):
    return {
        "task_id": task_id,
        "subtask_id": subtask_id,
        "message": f"Subtask {subtask_id} for task {task_id} requested"
    }