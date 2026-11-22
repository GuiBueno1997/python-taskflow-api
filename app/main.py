
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

# Creating our API application
app = FastAPI(
    title="TaskFlow API",
    description="A RESTful Task Management API built with Python",
    version="1.0.0"
)

tasks = [
    {"id": 1, "title": "Study Python", "description": "Learn the basics of Python", "completed": False},
    {"id": 2, "title": "Study FastAPI", "completed": True},
    {"id": 3, "title": "Study SQL", "completed": False}
]

# Task model
class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool

# Model for partial task updates
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


# Create a new task
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }

    tasks.append(new_task)

    return new_task

# Update PUT a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskCreate):

    for task in tasks:
        if task["id"] == task_id:

            task["title"] = updated_task.title
            task["description"] = updated_task.description
            task["completed"] = updated_task.completed

            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

# Update PATCH a task
@app.patch("/tasks/{task_id}")
def partial_update_task(task_id: int, updated_task: TaskUpdate):

    for task in tasks:
        if task["id"] == task_id:

            updated_data = updated_task.model_dump(exclude_unset=True)

            for field, value in updated_data.items():
                task[field] = value

            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)

            return {
                "message": "Task deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
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

# Get all tasks
@app.get("/tasks")
def list_tasks(completed: bool | None = None, limit: int = 10):

    filtered_tasks = tasks.copy()

    if completed is not None:
        filtered_tasks = [
            task for task in filtered_tasks
            if task["completed"] == completed
        ]

    return filtered_tasks[:limit]

# Get a specific task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

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



