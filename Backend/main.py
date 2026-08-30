import sqlite3
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "backend" / "tasks.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


init_db()


class TaskCreate(BaseModel):
    text: str


class TaskUpdate(BaseModel):
    done: bool


@app.get("/api/tasks")
def get_tasks():
    conn = get_db()
    rows = conn.execute("SELECT id, text, done FROM tasks ORDER BY id").fetchall()
    conn.close()
    return [{"id": r["id"], "text": r["text"], "done": bool(r["done"])} for r in rows]


@app.post("/api/tasks")
def create_task(task: TaskCreate):
    conn = get_db()
    cursor = conn.execute("INSERT INTO tasks (text, done) VALUES (?, 0)", (task.text,))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "text": task.text, "done": False}


@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    conn = get_db()
    result = conn.execute("UPDATE tasks SET done = ? WHERE id = ?", (int(update.done), task_id))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task_id, "done": update.done}


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db()
    result = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": task_id}


app.mount("/", StaticFiles(directory=BASE_DIR / "frontend", html=True), name="frontend")