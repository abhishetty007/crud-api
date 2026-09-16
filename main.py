from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

import repository
from supabase_client import supabase


app = FastAPI()


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)
    done: bool


class AuthRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks",
            "/auth/signup",
            "/auth/login",
            "/public/info",
            "/protected/profile"
        ]
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


# -------------------------
# Task endpoints
# -------------------------

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


# -------------------------
# Authentication endpoints
# -------------------------

@app.post("/auth/signup", status_code=201)
def signup(auth_data: AuthRequest):
    try:
        response = supabase.auth.sign_up({
            "email": auth_data.email,
            "password": auth_data.password
        })

        return response.model_dump()

    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Unable to create account"}
        )


@app.post("/auth/login")
def login(auth_data: AuthRequest):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": auth_data.email,
            "password": auth_data.password
        })

        return response.model_dump()

    except Exception:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid login credentials"}
        )


# -------------------------
# Stage 2: Public route
# -------------------------

@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }


# -------------------------
# Stage 2: Protected route
# -------------------------

@app.get("/protected/profile")
def protected_profile(request: Request):
    authorization = request.headers.get("Authorization")

    # No Authorization header
    if not authorization:
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"}
        )

    # Check Bearer <token> format
    parts = authorization.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"}
        )

    token = parts[1]

    if not token:
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"}
        )

    # Verify the token with Supabase
    try:
        response = supabase.auth.get_user(token)

        user = response.user

        return {
            "id": user.id,
            "email": user.email,
            "user_metadata": user.user_metadata
        }

    except Exception:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid or expired token"}
        )


# -------------------------
# Validation error handler
# -------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"}
    )