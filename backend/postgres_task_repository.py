from app import Task, TaskCreate, TaskUpdate
import db

class PostgresTaskRepository:
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
            return Task(id=db_task.id, title=db_task.title, completed=db_task.completed, priority=db_task.priority)

    def get(self, task_id: int) -> Task | None:
        with db.SessionLocal() as session:
            db_task = session.get(db.Task, task_id)
            if db_task is None:
                return None
            return Task(id=db_task.id, title=db_task.title, completed=db_task.completed, priority=db_task.priority)

    def list(self) -> list[Task]:
        with db.SessionLocal() as session:
            tasks_list: list[Task] = []
            db_tasks = session.query(db.Task).all()
            for db_task in db_tasks:
                tasks_list.append(Task(id=db_task.id, title=db_task.title, completed=db_task.completed, priority=db_task.priority))
            return tasks_list
    
    def update(self, task_id: int, task_update: TaskUpdate) -> Task | None:
        with db.SessionLocal() as session:
            db_task = session.get(db.Task, task_id)
            if db_task is None:
                return None
            updates = task_update.model_dump(exclude_unset=True)
            for field, value in updates.items():
                setattr(db_task, field, value)

            session.commit()
            session.refresh(db_task)

            return Task(id=db_task.id, title=db_task.title, completed=db_task.completed, priority=db_task.priority)

    def delete(self, task_id: int) -> bool:
        with db.SessionLocal() as session:
            db_task = session.get(db.Task, task_id)
            if db_task is None:
                return False

            session.delete(db_task)
            session.commit()
            return True