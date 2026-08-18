from typing import Literal
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False
    priority: Literal["low", "medium", "high"] = "medium"


class TaskCreate(BaseModel):
    title: str
    completed: bool = False
    priority: Literal["low", "medium", "high"] = "medium"

class Tag(BaseModel):
    id: int
    name: str

class TagCreate(BaseModel):
    name: str

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
    priority: Literal["low", "medium", "high"] | None = None

class TagUpdate(BaseModel):
    name: str | None = None

class ReadFile(BaseModel):
    content: str

class TaskRepository:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(self, task_create: TaskCreate) -> Task:
        task = Task(id=self._next_id, title=task_create.title, completed=task_create.completed, priority=task_create.priority)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def list(self) -> list[Task]:
        return list(self._tasks.values())

    def update(self, task_id: int, task_update: TaskUpdate) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        updated = task.model_copy(update=task_update.model_dump(exclude_unset=True))
        self._tasks[task_id] = updated
        return updated

    def delete(self, task_id: int) -> bool:
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True

class TagRepository:
    def __init__(self):
        self._tags: dict[int, Tag] = {}
        self._next_id = 1

    def add(self, tag_create: TagCreate) -> Tag:
        tag = Tag(id=self._next_id, name=tag_create.name)
        self._tags[tag.id] = tag
        self._next_id += 1
        return tag

    def get(self, tag_id: int) -> Tag | None:
        return self._tags.get(tag_id)

    def list(self) -> list[Tag]:
        return list(self._tags.values())

    def update(self, tag_id: int, tag_update: TagUpdate) -> Tag | None:
        tag = self._tags.get(tag_id)
        if tag is None:
            return None
        updated = tag.model_copy(update=tag_update.model_dump(exclude_unset=True))
        self._tags[tag_id] = updated
        return updated

    def delete(self, tag_id: int) -> bool:
        if tag_id not in self._tags:
            return False
        del self._tags[tag_id]
        return True

class TaskTagRepository:
    def __init__(self):
        self._task_tags: dict[int, set[int]] = {}

    def add_tag(self, task_id: int, tag_id: int) -> None: 
        if task_id not in self._task_tags:
            self._task_tags[task_id] = set()
        
        self._task_tags[task_id].add(tag_id)

    def remove_tag(self, task_id, tag_id) -> bool:
        if task_id not in self._task_tags:
            return False
        self._task_tags[task_id].discard(tag_id)
        return True

    def get_tags_for_task(self, task_id) -> set[int] | None:
        if task_id not in self._task_tags:
            return None
        return self._task_tags[task_id]

class TaskService:
    def __init__(self, repository: TaskRepository):
        self._repository = repository

    def create_task(self, task_create: TaskCreate) -> Task:
        return self._repository.add(task_create)

    def get_task(self, task_id: int) -> Task:
        task = self._repository.get(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return task

    def list_tasks(self) -> list[Task]:
        return self._repository.list()

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        task = self._repository.update(task_id, task_update)
        if task is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return task

    def delete_task(self, task_id: int) -> None:
        if not self._repository.delete(task_id):
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# Module-level singleton: Depends() creates a *new* TaskService per request,
# but every request needs to see the *same* tasks, so the repository itself
# has to live outside the per-request-created objects.
_repository = TaskRepository()


def get_task_service() -> TaskService:
    return TaskService(_repository)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_create: TaskCreate, service: TaskService = Depends(get_task_service)):
    return service.create_task(task_create)


@app.get("/tasks", response_model=list[Task])
def list_tasks(service: TaskService = Depends(get_task_service)):
    return service.list_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    return service.get_task(task_id)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int, task_update: TaskUpdate, service: TaskService = Depends(get_task_service)
):
    return service.update_task(task_id, task_update)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    service.delete_task(task_id)


@app.get("/readRosetta", response_model=ReadFile)
def read_rosetta():
    try:
        with open(Path(__file__).parent.parent / "ROSETTA.md") as f:
            text = f.read()
        return {"content": text}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
