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

2. **Create environment file:**
   Create a `.env` file in the root directory with the following constants:
   ```env
   SECRET_KEY=your_secret_key_here
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
   > **Note:** Replace `your_secret_key_here` with a secure secret key. You can generate one using:
   > ```bash
   > openssl rand -hex 32
   > ```

3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn sqlalchemy bcrypt python-jose python-multipart
   ```

4. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the app:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /auth/` - Register new user
- `POST /auth/token` - Login

### Todos
- `GET /todos/` - Get all todos
- `POST /todos/` - Create todo
- `PUT /todos/{id}` - Update todo
- `DELETE /todos/{id}` - Delete todo

### User Management
- `GET /user/` - Get current user details (admin only)
- `PUT /user/password` - Change password (admin only)

## Tech Stack

- FastAPI
- SQLite + SQLAlchemy (with PostgreSQL option available)
- JWT Authentication
- Alembic for database migrations

---
*Created: September 2025*