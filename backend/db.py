from sqlalchemy import Boolean, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    completed: Mapped[bool] = mapped_column(Boolean)
    priority: Mapped[str] = mapped_column(String(25))

engine = create_engine(os.environ["DATABASE_URL"])
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)