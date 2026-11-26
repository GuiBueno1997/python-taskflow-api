
from app.database import SessionLocal
from app.models import Task

db = SessionLocal()

try:
    title = input("Enter task title: ")
    description = input("Enter task description: ")

    new_task = Task(
        title=title,
        description=description,
        completed=False
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    print(f"Task {new_task.id} created successfully!")

except Exception:
    db.rollback()
    raise

finally:
    db.close()
