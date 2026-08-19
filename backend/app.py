from typing import Literal
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path


class Tag(BaseModel):
    id: int
    name: str

class TagCreate(BaseModel):
    name: str

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False
    priority: Literal["low", "medium", "high"] = "medium"
    tags: list[Tag] = []

class TaskCreate(BaseModel):
    title: str
    completed: bool = False
    priority: Literal["low", "medium", "high"] = "medium"

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
    def __init__(self, repository: TaskRepository, tag_repository: TagRepository, tasktag_repository: TaskTagRepository):
        self._repository = repository
        self._tag_repository = tag_repository
        self._tasktag_repository = tasktag_repository

    def create_task(self, task_create: TaskCreate) -> Task:
        return self._repository.add(task_create)

    def get_task(self, task_id: int) -> Task:
        task = self._repository.get(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        task = self._hydrate_tasks(task)
        return task

    def list_tasks(self) -> list[Task]:
        list_tasks = self._repository.list()
        new_list: list[Task] = []
        for task in list_tasks:
            task = self._hydrate_tasks(task)
            new_list.append(task)
        return new_list

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        task = self._repository.update(task_id, task_update)
        if task is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return task

    def delete_task(self, task_id: int) -> None:
        if not self._repository.delete(task_id):
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    def _hydrate_tasks(self, task: Task) -> Task:
        tag_id_list = self._tasktag_repository.get_tags_for_task(task.id)
        if tag_id_list is None:
            tag_id_list = []
            
        tags: list[Tag] = []
        for tag_id in tag_id_list:
            tag = self._tag_repository.get(tag_id)
            tags.append(tag)
        task = task.model_copy(update={"tags": tags})
        return task

    def attach_tag(self, task_id: int, tag_id: int) -> Task:
        task = self._repository.get(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        tag = self._tag_repository.get(tag_id)
        if tag is None:
            raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")
        self._tasktag_repository.add_tag(task_id, tag_id)
        task = self._hydrate_tasks(task)
        return task
    
    def detach_tag(self, task_id: int, tag_id: int) -> Task:
        task = self._repository.get(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        tag = self._tag_repository.get(tag_id)
        if tag is None:
            raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")
        self._tasktag_repository.remove_tag(task_id, tag_id)
        task = self._hydrate_tasks(task)
        return task

class TagService:
    def __init__(self, tag_repository: TagRepository):
        self._tag_repository = tag_repository

    def create_tag(self, tag_create: TagCreate) -> Tag:
        return self._tag_repository.add(tag_create)

    def get_tag(self, tag_id: int) -> Tag:
        tag = self._tag_repository.get(tag_id)
        if tag is None:
            raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")
        return tag

    def list_tags(self) -> list[Tag]:
        return self._tag_repository.list()

    def update_tag(self, tag_id: int, tag_update: TagUpdate) -> Tag:
        tag = self._tag_repository.update(tag_id, tag_update)
        if tag is None:
            raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")
        return tag

    def delete_tag(self, tag_id: int) -> None:
        if not self._tag_repository.delete(tag_id):
            raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")


# Module-level singleton: Depends() creates a *new* TaskService per request,
# but every request needs to see the *same* tasks, so the repository itself
# has to live outside the per-request-created objects.
_repository = TaskRepository()
_tag_repository = TagRepository()
_tasktag_repository = TaskTagRepository()


def get_task_service() -> TaskService:
    return TaskService(_repository, _tag_repository, _tasktag_repository)

def get_tag_service() -> TagService:
    return TagService(_tag_repository)

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

@app.post("/tags", response_model=Tag, status_code=201)
def create_tag(tag_create: TagCreate, service: TagService = Depends(get_tag_service)):
    return service.create_tag(tag_create)

@app.get("/tags", response_model=list[Tag])
def list_tags(service: TagService = Depends(get_tag_service)):
    return service.list_tags()

@app.get("/tags/{tag_id}", response_model=Tag)
def get_tag(tag_id: int, service: TagService = Depends(get_tag_service)):
    return service.get_tag(tag_id)

@app.put("/tags/{tag_id}", response_model=Tag)
def update_tag(
    tag_id: int, tag_update: TagUpdate, service: TagService = Depends(get_tag_service)
):
    return service.update_tag(tag_id, tag_update)

@app.delete("/tags/{tag_id}", status_code=204)
def delete_tag(tag_id: int, service: TagService = Depends(get_tag_service)):
    service.delete_tag(tag_id)

@app.post("/tasks/{task_id}/tags/{tag_id}", response_model=Task)
def attach_tag(task_id: int, tag_id: int, service: TaskService = Depends(get_task_service)):
    return service.attach_tag(task_id, tag_id)

@app.delete("/tasks/{task_id}/tags/{tag_id}", response_model=Task)
def detach_tag(task_id: int, tag_id: int, service: TaskService = Depends(get_task_service)):
    return service.detach_tag(task_id, tag_id)