from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from models import Users
from starlette import status
from passlib.context import CryptContext
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from authlib.jose import jwt, JoseError
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = os.getenv("SECRET_KEY")
HEADER = {"alg": "HS256", "typ": "JWT"}
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

db_dependency = Annotated[Session, Depends(get_db)]


class CreateUserRequest(BaseModel):  # baseModel return what kind of type should pass
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

    model_config = {
        "extra": "forbid",  # Prevents unexpected fields in request
        "json_schema_extra": {
            "example": {
                "email": "exam@example.com",
                "username": "example",
                "first_name": "example",
                "last_name": "one",
                "password": "exam123",
                "role": "user",
                "phone_number": "1234567890"
            }
        },
    }


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(username: str, user_id: int, user_role:str, expires_delta: timedelta):
    PAYLOAD = {"sub": username, "id": user_id, "role":user_role}
    expires = datetime.now(timezone.utc) + expires_delta
    PAYLOAD.update({"exp": expires})
    token = jwt.encode(HEADER, PAYLOAD, SECRET_KEY)
    return token


async def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role:str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return {"username": username, "id": user_id, "role":user_role}
    except JoseError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,  # we have to assign each as hashed password and password is diff in baseModel class and actual class
        username=create_user_request.username,  # therefore cant use Todos(**create_user_request.model_dump())
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        role=create_user_request.role,
        phone_number=create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": token, "token_type": "bearer"}
