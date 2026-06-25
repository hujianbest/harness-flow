"""
Authentication endpoints.
"""
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.schemas import TokenResponse, UserLogin, UserRegister

router = APIRouter()
security = HTTPBearer()

# Mock user storage (replace with database in production)
mock_users: dict = {}


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def register(user_data: UserRegister) -> dict:
    """
    Register a new user.

    - **email**: User email address
    - **password**: User password (8-64 characters)
    - **name**: User display name (1-50 characters)
    """
    email = user_data.email
    password = user_data.password
    name = user_data.name

    # Check if user exists
    if email in mock_users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "CONFLICT_ERROR",
                    "message": "Email already registered",
                    "details": {"field": "email", "issue": "already in use"},
                }
            },
        )

    # Create user
    user_id = uuid4()
    mock_users[email] = {
        "id": user_id,
        "email": email,
        "password_hash": get_password_hash(password),
        "name": name,
    }

    # Create tokens
    token = create_access_token({"sub": str(user_id), "email": email})
    refresh_token = create_access_token({"sub": str(user_id), "type": "refresh"})

    return {"userId": user_id, "token": token, "refreshToken": refresh_token}


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin) -> dict:
    """
    User login.

    - **email**: User email address
    - **password**: User password
    """
    email = credentials.email
    password = credentials.password

    # Find user
    user = mock_users.get(email)
    if not user or not verify_password(password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "UNAUTHORIZED_ERROR",
                    "message": "Invalid email or password",
                }
            },
        )

    # Create tokens
    token = create_access_token({"sub": str(user["id"]), "email": email})
    refresh_token = create_access_token({"sub": str(user["id"]), "type": "refresh"})

    return {"userId": user["id"], "token": token, "refreshToken": refresh_token}


@router.post("/logout")
async def logout(credentials: Annotated[HTTPAuthorizationCredentials, security]) -> dict:
    """
    User logout.
    """
    # In production, add token to blacklist
    return {"message": "Logged out successfully"}
