# Task API

A small CRUD API built with Python, FastAPI, PostgreSQL, and Docker Compose.

The project manages a simple list of tasks and demonstrates how an API can use a separate repository layer for database access.

## Architecture

```text
Client
  |
  v
FastAPI application
  |
  v
repository.py
  |
  v
PostgreSQL
  |
  v
Docker volume
The FastAPI routes are separated from database access. The routes call functions in repository.py, while the repository handles PostgreSQL queries.

Technologies
Python
FastAPI
PostgreSQL
psycopg
Docker
Docker Compose
Project Structure
.
├── main.py
├── repository.py
├── init.sql
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── docs/
Configuration

Database configuration is stored in environment variables.

The real .env file is intentionally excluded from Git using .gitignore.

A safe template is provided in:

.env.example

Example:

POSTGRES_USER=taskuser
POSTGRES_PASSWORD=your_password_here
POSTGRES_DB=taskdb
DATABASE_URL=postgresql://taskuser:your_password_here@db:5432/taskdb

Inside Docker Compose, db is the hostname of the PostgreSQL service.

Database

PostgreSQL runs inside Docker using the official PostgreSQL image.

The database uses a named Docker volume:

taskdata

This keeps PostgreSQL data persistent when the database container is stopped or recreated.

The database table is created automatically using:

init.sql

The schema is:

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);
Running the Project

Make sure Docker Desktop is running.

Start the complete stack with:

docker compose up --build

This starts:

FastAPI application
PostgreSQL database

The API is available at:

http://localhost:8000

Swagger UI:

http://localhost:8000/docs
API Endpoints
Method	Endpoint	Description
GET	/	API information
GET	/health	Health check
GET	/tasks	Get all tasks
GET	/tasks/{id}	Get one task
POST	/tasks	Create a task
PUT	/tasks/{id}	Update a task
DELETE	/tasks/{id}	Delete a task
Example Task
{
  "id": 1,
  "title": "Learn Docker",
  "done": false
}
Repository Layer

Database operations are kept in repository.py.

For example, creating a task calls:

FastAPI route
    ↓
repository.create_task()
    ↓
PostgreSQL INSERT

This keeps the API layer independent from the database implementation.

SQL queries use parameters instead of directly concatenating user input.

Persistence Test

Persistence was tested by:

Starting the application and PostgreSQL with Docker Compose.
Creating a task through the API.
Confirming the task existed in PostgreSQL.
Running docker compose down.
Starting the stack again with docker compose up --build.
Requesting GET /tasks.
Confirming the previously created task was still present.

The PostgreSQL data survives because the database uses the named taskdata Docker volume.

docker compose down -v should not be used when testing persistence because it removes the named volume.

Useful Database Command

To inspect the tasks directly in PostgreSQL:

docker compose exec db psql -U taskuser -d taskdb -c "SELECT * FROM tasks;"
HTTP Status Codes
Status	Meaning
200	Successful request
201	Task created
204	Task deleted successfully
400	Invalid request
404	Task not found