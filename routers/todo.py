from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from models import Todos
from pydantic import BaseModel, Field
from starlette import status
from database import get_db
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

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
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenicate failed"
        )
    return (
        db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
    )  # rertieving the values as per user owner id  owner_id is our foreign key of user's id


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenicate failed"
        )
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todos", status_code=status.HTTP_200_OK)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodoRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenicate failed"
        )
    todo_model = Todos(
        **todo_request.model_dump(), owner_id=user.get("id")
    )  # as user is dict use get to retrieve id
    db.add(todo_model)
    db.commit()


@router.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="not found")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
