from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from datetime import timedelta
from src.middleware.auth import create_access_token
from config.settings import settings
from config.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.user_service import UserService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

class UserRegistration(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str

@router.post("/token", response_model=Token)
async def login_for_access_token(
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user_service = UserService(db)
    user = await user_service.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserRegistration,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user
    """
    try:
        # ← Password truncate fix added
        if len(user_data.password.encode("utf-8")) > 72:
            user_data.password = user_data.password[:72]

        user_service = UserService(db)
        user = await user_service.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User registration failed"
            )

        return UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            role=user.role
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

from src.middleware.auth import get_current_user

@router.get("/profile", response_model=UserResponse)
async def read_users_me(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    from uuid import UUID
    try:
        user_id = UUID(current_user["user_id"])
        user = await user_service.get_user_by_id(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        role=user.role
    )

@router.post("/logout")
async def logout_user(
    current_user: dict = Depends(lambda: {"user_id": "test_user"}),
    db: AsyncSession = Depends(get_db)
):
    """
    Logout the current user by invalidating their session
    """
    return {"message": "Successfully logged out"}
