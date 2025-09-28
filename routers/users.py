from fastapi import APIRouter, HTTPException, Path
from fastapi.params import Body, Depends
from pydantic import BaseModel, Field
from starlette import status
from typing import Annotated
from ..database import get_db
from .auth import get_current_user
from sqlalchemy.orm import Session
from ..models import Users
from passlib.context import CryptContext

# Create router for user-related endpoints with /user prefix
router=APIRouter(
    prefix="/user",
    tags=["user current details"]
)

# Pydantic model for password verification and update requests
class UserVerfication(BaseModel):
    password:str  # Current password for verification
    new_password:str = Field(min_length=6)  # New password (minimum 6 characters)

# Pydantic model for updating phone number
class UserPhoneNumber(BaseModel):
    phone_number:str = Field(min_length=10, max_length=10)
    
# Type annotations for dependency injection
user_dependency = Annotated[dict, Depends(get_current_user)]  # Gets current authenticated user
db_dependency = Annotated[Session, Depends(get_db)]  # Gets database session
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Password hashing context

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency):
    # Check if user is authenticated and has admin role
    if user is None or user.get('userrole') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed: You have to be Admin")
    
    # Query database to get user details by ID
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db:db_dependency, user_verification:UserVerfication):
    # Ensure user is authenticated and has admin privileges
    if user is None or user.get('userrole') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed: You have to be Admin")
    
    # Get the user record from database
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    # Verify the current password matches the stored hash
    # bcrypt_context.verify(plain_password, hashed_password) - ORDER MATTERS!
    # First param: plain text password entered by user
    # Second param: stored hashed password from database
    if  not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password verification for old")
    
    # Hash the new password using bcrypt
    hashed_new_password = bcrypt_context.hash(user_verification.new_password)
    
    # Update user's password in database
    user_model.hashed_password = hashed_new_password
    db.add(user_model)  # Mark the object as modified
    db.commit()  # Commit changes to database

@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user:user_dependency, db:db_dependency, phone_number:UserPhoneNumber):
    # Ensure user is authenticated and has admin privileges
    if user is None or user.get('userrole') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed: You have to be Admin")
    
    # Get the user record from database
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    # Update user's phone number in database
    user_model.phone_number = phone_number.phone_number
    db.add(user_model)  # Mark the object as modified
    db.commit()  # Commit changes to database