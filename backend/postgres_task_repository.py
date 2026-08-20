from app import Task, TaskCreate, TaskUpdate
from db import db.SessionLocal
from db import db.Task

def add(self, task_create: TaskCreate) -> Task:
    with db.SessionLocal() as session:
        db_task = db.Task(
            title=task_create.title,
            completed=task_create.completed,
            priority=task_create.priority,
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return Task(id=db_task.title, completed=db_task.completed, priority=db_task.priority)

def get(self, task_id: int) -> Task | None:
    