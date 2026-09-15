from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

import repository


app = FastAPI()


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)
    done: bool


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
    return repository.get_all_tasks()


@app.get("/tasks/{id}")
def get_task(id: int):
    task = repository.get_task(id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return task


@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    return repository.create_task(task_data.title)


@app.put("/tasks/{id}")
def update_task(id: int, task_data: TaskUpdate):
    task = repository.update_task(
        id,
        task_data.title,
        task_data.done
    )

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return task


@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    deleted = repository.delete_task(id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"}
    )