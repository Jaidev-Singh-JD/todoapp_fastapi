from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from ..models import Todos
from pydantic import BaseModel, Field
from starlette import status
from ..database import get_db
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter()

# Type annotations for dependency injection
db_dependency = Annotated[Session, Depends(get_db)]  # Database session dependency
user_dependency = Annotated[dict, Depends(get_current_user)]  # User authentication dependency


class TodoRequest(BaseModel):
    """Schema for Todo request validation"""
    title: str = Field(min_length=1)  # Title must have at least 1 character
    description: str = Field(min_length=1, max_length=100)  # Description length: 1-100 chars
    priority: int = Field(gt=0, lt=6)  # Priority must be between 1 and 5
    complete: bool  # Todo completion status

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "NEW TODO",
                "description": "THIS IS A NEW TODO",
                "priority": 3,
                "complete": False,
            }
        }
    }


@router.get("/", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency):
    """Get all todos for the authenticated user"""
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenicate failed")
    return (
        db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
    )  # Retrieving todos filtered by user's owner_id (foreign key)


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    """Get a specific todo by ID for the authenticated user"""
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenicate failed")
    todo_model = (
        db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    )  # Ensure user can only access their own todos
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todos", status_code=status.HTTP_200_OK)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodoRequest  # Make sure user is authenticated
):
    """Create a new todo for the authenticated user"""
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenicate failed")
    todo_model = Todos(
        **todo_request.model_dump(), owner_id=user.get("id")
    )  # Create todo with user's ID as owner_id (user is dict, use get() to retrieve id)
    db.add(todo_model)
    db.commit()


@router.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    db: db_dependency, user: user_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)
):
    """Update an existing todo by ID for the authenticated user"""
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenicate failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="not found")
    
    # Update todo fields with new values
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

 # Delete a todo by ID for the authenticated user
# This function ensures that only the owner of the todo (authenticated user) can delete it.
# It matches the `todo_id` with the `owner_id` from the JWT payload to verify ownership.
# If the todo does not exist or does not belong to the user, a 404 error is raised.
# After successful verification, the todo is deleted from the database.
@router.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenicate failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="not found")
    
    # Delete the todo from database
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()
