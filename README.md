# Domovoy

A standalone daily tasks tracker, built as a companion app to Spectre — a personal homelab dashboard. Domovoy runs as its own FastAPI service with a SQLite backend, so tasks persist server-side and stay in sync across any device that opens it.

## Features

- Add, check off, and delete daily tasks
  
- Tasks persist in a SQLite database — not just browser storage, so the list is the same whether you open it from your laptop, phone, or another device
  
- Lightweight FastAPI backend serving both the API and the static frontend
  
- Styled to match the Spectre dashboard's dark, ghost-themed aesthetic
  
## Tech stack

- Backend: FastAPI, SQLite (via Python's built-in sqlite3)
  
- Frontend: Vanilla HTML, CSS, and JavaScript (no framework)
  
- Server: Uvicorn (ASGI)

  
## Project Structure

```
Domovoy/
├── backend/
│   ├── main.py        # FastAPI app: API routes + static file serving
│   └── tasks.db        # SQLite database (created automatically on first run)
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

## Part of the Spectre ecosystem: https://github.com/Oliver-Tay23/Dashboard-Spectre#spectre

Domovoy is linked from the Spectre dashboard's "Daily Tasks" card, opening in a new tab. It's built as a separate project so it can be hosted, updated, and scaled independently of the main dashboard.
