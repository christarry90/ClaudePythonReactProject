from app import User, UserCreate
import db

class PostgresUserRepository:
    def add(self, username: str, hashed_password: str) -> User:
        with db.SessionLocal() as session:
            db_user = db.User(
                username=username,
                hashed_password=hashed_password,
            )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return User(id=db_user.id, username=db_user.username)

    def get_by_username(self, username: str) -> User | None:
        with db.SessionLocal() as session:
            db_user = session.query(db.User).filter(db.User.username == username).first()
            if db_user is None:
                return None
            return User(id=db_user.id, username=db_user.username)