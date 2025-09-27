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
   # Install all dependencies from requirements.txt
   pip install -r requirements.txt
   ```
   
   > **Alternative manual installation:**
   > ```bash
   > # Core dependencies
   > pip install fastapi uvicorn sqlalchemy bcrypt python-jose python-multipart alembic
   > 
   > # Development dependencies (optional but recommended)
   > pip install pytest
   > ```

4. **Initialize database (first time only):**
   ```bash
   # Option 1: Use Alembic migrations (recommended for production)
   alembic upgrade head
   
   # Option 2: Auto-creation (happens automatically when you run the app)
   # The app will create basic tables automatically, but won't include
   # schema changes from migrations like the phone_number column
   ```
   
   > **Note**: This app has both auto-creation and migration support:
   > - **Auto-creation**: Basic tables are created when the app starts
   > - **Migrations**: Include additional schema changes (like phone_number column)
   > - **For complete schema**: Run the migration command above

5. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the app:**
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

## Development

### Running Tests
The project includes a test suite using pytest:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest test/test_example.py
```

### Database Migrations
This project uses Alembic for database schema management:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Check current migration status
alembic current

# View migration history
alembic history
```

### Project Structure
```
TodoApp/
├── main.py              # FastAPI application entry point
├── models.py            # SQLAlchemy database models
├── database.py          # Database configuration
├── requirements.txt     # Python dependencies
├── routers/             # API route handlers
│   ├── auth.py         # Authentication routes
│   ├── todo.py         # Todo CRUD routes
│   ├── users.py        # User management routes
│   └── admin.py        # Admin-only routes
├── test/               # Test suite
│   └── test_example.py # Example test cases
├── alembic/            # Database migration files
└── .env               # Environment variables (create manually)
```

## Tech Stack

- FastAPI
- SQLite + SQLAlchemy (with PostgreSQL option available)
- JWT Authentication
- Alembic for database migrations

---
*Created: September 2025*