# Task API

A small CRUD API built with Python and FastAPI.

The API manages an in-memory to-do list and supports creating, reading, updating, and deleting tasks.

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- SQLite

## Installation and Run

Create a virtual environment:

```bash
python -m venv .venv

Activate it on Windows PowerShell:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Start the server:

uvicorn main:app --reload

The API will be available at:

http://127.0.0.1:8000

Swagger UI

Interactive API documentation is available at:

http://127.0.0.1:8000/docs

Endpoints
Method	Endpoint	Description
GET	/	Get API information
GET	/health	Check API health
GET	/tasks	Get all tasks
GET	/tasks/{id}	Get one task
POST	/tasks	Create a task
PUT	/tasks/{id}	Update a task
DELETE	/tasks/{id}	Delete a task
Task Format

A task contains:

{
  "id": 1,
  "title": "Complete assignment",
  "done": false
}
Why SQLite?

SQLite was chosen because it is lightweight, requires no separate database server, and stores the database in a single file. This makes it simple to set up while still providing persistence when the server restarts.

Database

The application uses a SQLite database stored in:

tasks.db

The database file is created automatically when the application starts if it does not already exist.

The tasks table is also created automatically. Three example tasks are inserted only when the table is empty.

The database file is included in .gitignore, so it is not uploaded to GitHub.

Data Persistence

Unlike the previous in-memory version, tasks stored in SQLite survive server restarts.

The API endpoints remain the same while the storage implementation has changed from a Python list to a SQLite database.

HTTP Status Codes
Status	Meaning
200	Successful request
201	Task successfully created
204	Task successfully deleted
400	Invalid request
404	Task not found
Example curl Output
HTTP/1.1 200 OK
date: Sun, 13 Sep 2026 13:20:05 GMT
server: uvicorn
content-length: 15
content-type: application/json
Example SQL Query

During Stage 4, I ran the following query in DB Browser for SQLite:

SELECT * FROM tasks WHERE done = 1;

This query returns only the tasks that are marked as completed.

Database Screenshot

The SQLite database was inspected using DB Browser for SQLite.

Swagger Screenshot

The API can be tested interactively using FastAPI's Swagger UI.


### One small correction

The first line currently says:

> "The API manages an in-memory to-do list"

That's technically outdated now because **W3 A1 has moved the storage to SQLite**.

Change that sentence to:

```markdown
The API manages a SQLite-backed to-do list and supports creating, reading, updating, and deleting tasks.

So your final opening becomes:

# Task API

A small CRUD API built with Python and FastAPI.

The API manages a SQLite-backed to-do list and supports creating, reading, updating, and deleting tasks.