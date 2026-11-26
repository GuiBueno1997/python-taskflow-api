
from app.database import SessionLocal
from app.models import Task

db = SessionLocal()

try:
    tasks = db.query(Task).all()

    for task in tasks:
        print(
            f"ID: {task.id} | "
            f"Title: {task.title} | "
            f"Completed: {task.completed}"
        )

finally:
    db.close()
