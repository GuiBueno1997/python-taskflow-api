
from app.database import SessionLocal
from app.models import Task

db = SessionLocal()

try:
    task_id = int(input("Enter the task ID to delete: "))

    task = db.query(Task).filter(Task.id == task_id).first()

    if task:
        db.delete(task)
        db.commit()
        print(f"Task {task_id} deleted successfully!")
    else:
        print("Task not found!")

except Exception:
    db.rollback()
    raise

finally:
    db.close()
