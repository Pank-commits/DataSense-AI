from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.auth import (
    UserRegister,
    UserLogin,
    AuthResponse,
    UserResponse,
)

from app.services.auth_services import (
    register_user,
    login_user,
)

from app.core.security import (
    get_current_user,
)

from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================
# Register
# ==========================

@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=201,
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):

    return register_user(
        db,
        user,
    )


# ==========================
# Login
# ==========================

@router.post(
    "/login",
    response_model=AuthResponse,
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):

    return login_user(
        db,
        user,
    )


# ==========================
# Current User
# ==========================

@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(
        get_current_user
    )
):

    return current_user