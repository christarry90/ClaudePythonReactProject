from app import Task, TaskCreate, TaskUpdate
import db

class PostgresTaskRepository:
    def add(self, task_create: TaskCreate, user_id: int) -> Task:
        with db.SessionLocal() as session:
            db_task = db.Task(
                title=task_create.title,
                completed=task_create.completed,
                priority=task_create.priority,
                user_id=user_id,
            )
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            return Task(id=db_task.id, title=db_task.title, completed=db_task.completed, priority=db_task.priority, user_id=db_task.user_id)

    def get(self, task_id: int, user_id: int) -> Task | None:
        with db.SessionLocal() as session:
            db_task = session.query(db.Task).filter(db.Task.id==task_id, db.Task.user_id==user_id ).first()
            if db_task is None:
                return None
            return Task(id=db_task.id, title=db_task.title, completed=db_task.completed, priority=db_task.priority, user_id=db_task.user_id)

    def list(self, user_id: int) -> list[Task]:
        with db.SessionLocal() as session:
            tasks_list: list[Task] = []
            db_tasks = session.query(db.Task).filter(db.Task.user_id==user_id ).all()
            for db_task in db_tasks:
                tasks_list.append(Task(id=db_task.id, title=db_task.title, completed=db_task.completed, priority=db_task.priority, user_id=db_task.user_id))
            return tasks_list
    
    def update(self, task_id: int, user_id: int, task_update: TaskUpdate) -> Task | None:
        with db.SessionLocal() as session:
            db_task = session.query(db.Task).filter(db.Task.id==task_id, db.Task.user_id==user_id ).first()
            if db_task is None:
                return None
            updates = task_update.model_dump(exclude_unset=True)
            for field, value in updates.items():
                setattr(db_task, field, value)

            session.commit()
            session.refresh(db_task)

            return Task(id=db_task.id, title=db_task.title, completed=db_task.completed, priority=db_task.priority, user_id= db_task.user_id)

    def delete(self, task_id: int, user_id: int) -> bool:
        with db.SessionLocal() as session:
            db_task = session.query(db.Task).filter(db.Task.id==task_id, db.Task.user_id==user_id ).first()
            if db_task is None:
                return False

            session.delete(db_task)
            session.commit()
            return True