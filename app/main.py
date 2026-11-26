
from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task

from app.schemas import TaskCreate, TaskUpdate, TaskResponse

# Creating our API application
app = FastAPI(
    title="TaskFlow API",
    description="A RESTful Task Management API built with Python",
    version="1.0.0"
)

# Create a new task 2.0
@app.post("/tasks", status_code=201, response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

# Update PUT a task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db)
):
    # 1. Buscar a tarefa pelo ID

    task = db.query(Task).filter(Task.id == task_id).first()
    # 2. Verificar se ela existe
    if task:
        # 3. Atualizar title, description e completed

        task.title = updated_task.title
        task.description = updated_task.description
        task.completed = updated_task.completed

        # 4. Salvar as alterações no banco

        db.commit()

        # 5. Atualizar os dados do objeto

        db.refresh(task)

        # 6. Retornar a tarefa

        return task

    # 7. Se não encontrar, retornar HTTP 404
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

# Update PATCH a task
@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def partial_update_task(
    task_id: int,
    updated_task: TaskUpdate,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(Task.id == task_id).first()

    if task:

        updated_data = updated_task.model_dump(exclude_unset=True)

        if not updated_data:
            raise HTTPException(
                status_code=422,
                detail="At least one field must be provided"
            )

        for field, value in updated_data.items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)

        return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if task:
        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully!"}

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
@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(
    completed: bool | None = None,
    limit: int = Query(default=10, gt=0, le=100),
    db: Session = Depends(get_db)):

    query = db.query(Task)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    query = query.limit(limit)

    tasks = query.all()

    return tasks

# Get a specific task
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if task:
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
    limit: int = Query(default=10, gt=0, le=100),
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



