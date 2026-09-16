from fastapi import FastAPI, Request, Depends, HTTPException
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


# -------------------------
# Reusable authentication dependency
# -------------------------

def get_current_user(request: Request):
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    parts = authorization.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    token = parts[1]

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    try:
        response = supabase.auth.get_user(token)

        return response.user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks",
            "/auth/signup",
            "/auth/login",
            "/auth/logout",
            "/public/info",
            "/protected/profile",
            "/protected/dashboard"
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


@app.post("/auth/logout", status_code=204)
def logout(user=Depends(get_current_user)):
    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    return


# -------------------------
# Public route
# -------------------------

@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }


# -------------------------
# Protected routes
# -------------------------

@app.get("/protected/profile")
def protected_profile(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "user_metadata": user.user_metadata
    }


@app.get("/protected/dashboard")
def protected_dashboard(user=Depends(get_current_user)):
    return {
        "message": "Welcome to your dashboard!",
        "user_id": user.id,
        "email": user.email
    }
@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
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