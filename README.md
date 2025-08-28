# TodoApp FastAPI

> ⚠️ **Under Development** - This project is currently in development and may undergo changes.

A simple Todo application built with FastAPI featuring user authentication and task management.

## Features

- User authentication (register/login)
- Create, read, update, and delete todos
- SQLite database
- RESTful API

## Quick Start

1. **Clone and setup:**
   ```bash
   git clone https://github.com/Jaidev-Singh-JD/todoapp-fastapi.git
   cd TodoApp
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn sqlalchemy bcrypt python-jose python-multipart
   ```

3. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the app:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /auth/create/user` - Register new user
- `POST /auth/token` - Login

### Todos
- `GET /todos/` - Get all todos
- `POST /todos/` - Create todo
- `PUT /todos/{id}` - Update todo
- `DELETE /todos/{id}` - Delete todo

## Tech Stack

- FastAPI
- SQLite + SQLAlchemy
- JWT Authentication

---
*Created: August 2025*