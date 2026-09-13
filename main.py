from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field

app = FastAPI()


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)
    done: bool


tasks = [
    {"id": 1, "title": "Complete assignment", "done": False},
    {"id": 2, "title": "Study FastAPI", "done": True},
    {"id": 3, "title": "Push code to GitHub", "done": False}
]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"}
    )


@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )


@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    new_id = max(task["id"] for task in tasks) + 1

    new_task = {
        "id": new_id,
        "title": task_data.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{id}")
def update_task(id: int, task_data: TaskUpdate):
    for task in tasks:
        if task["id"] == id:
            task["title"] = task_data.title
            task["done"] = task_data.done
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )


@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )