from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()

tasks = [
    {"id": 1, "title": "Complete assignment", "done": False},
    {"id": 2, "title": "Study FastAPI", "done": True},
    {"id": 3, "title": "Push code to GitHub", "done": False}
]


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

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )