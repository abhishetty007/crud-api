import sqlite3

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field

app = FastAPI()
DB_NAME = "tasks.db"


def init_db():
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    cursor = connection.execute("SELECT COUNT(*) FROM tasks")
    task_count = cursor.fetchone()[0]

    if task_count == 0:
        connection.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Complete assignment", False),
                ("Study FastAPI", True),
                ("Push code to GitHub", False)
            ]
        )

    connection.commit()
    connection.close()


init_db()


def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)
    done: bool


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
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


@app.get("/tasks/{id}")
def get_task(id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    connection.close()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return dict(row)


@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    connection = get_connection()

    cursor = connection.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task_data.title, False)
    )

    new_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "id": new_id,
        "title": task_data.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{id}")
@app.put("/tasks/{id}")
def update_task(id: int, task_data: TaskUpdate):
    connection = get_connection()

    cursor = connection.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (task_data.title, task_data.done, id)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    connection.close()

    return dict(row)


@app.delete("/tasks/{id}", status_code=204)
@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return