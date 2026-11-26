
from app.database import SessionLocal
from app.models import Task

db = SessionLocal()

try:
    task_id = int(input("Enter the task ID to update: "))

    task = db.query(Task).filter(Task.id == task_id).first()

    if task:
        print(f"Current title: {task.title}")

        new_title = input("Enter new title: ")
        new_completed = input("Completed? (yes/no): ").lower()

        task.title = new_title
        task.completed = new_completed == "yes"

        db.commit()
        db.refresh(task)

        print(f"Task {task.id} updated successfully!")
    else:
        print("Task not found!")

except Exception:
    db.rollback()
    raise

finally:
    db.close()
