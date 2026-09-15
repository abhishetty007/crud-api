import os

import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def get_all_tasks():
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, title, done FROM tasks ORDER BY id"
        )
        rows = cursor.fetchall()

    connection.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }
        for row in rows
    ]


def get_task(task_id):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, title, done FROM tasks WHERE id = %s",
            (task_id,)
        )
        row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


def create_task(title):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            RETURNING id
            """,
            (title, False)
        )

        task_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    return {
        "id": task_id,
        "title": title,
        "done": False
    }


def update_task(task_id, title, done):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE tasks
            SET title = %s, done = %s
            WHERE id = %s
            RETURNING id, title, done
            """,
            (title, done, task_id)
        )

        row = cursor.fetchone()

    connection.commit()
    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


def delete_task(task_id):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )

        deleted = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted > 0