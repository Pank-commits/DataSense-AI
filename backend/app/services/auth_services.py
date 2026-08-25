from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.auth import (
    UserRegister,
    UserLogin,
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


# ==========================
# Register User
# ==========================

def register_user(
    db: Session,
    user: UserRegister,
):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered."
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(
        {"sub": new_user.email}
    )

    return {
        "message": "Registration successful",

        "access_token": token,

        "token_type": "bearer",

        "user": {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email,
            "role": new_user.role,
            "created_at": new_user.created_at,
        },
    }


# ==========================
# Login User
# ==========================

def login_user(
    db: Session,
    user: UserLogin,
):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not verify_password(
        user.password,
        existing_user.password,
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token = create_access_token(
        {"sub": existing_user.email}
    )

    return {

        "message": "Login successful",

        "access_token": token,

        "token_type": "bearer",

        "user": {
            "id": existing_user.id,
            "full_name": existing_user.full_name,
            "email": existing_user.email,
            "role": existing_user.role,
            "created_at": existing_user.created_at,
        },
    }


# ==========================
# Get User By Email
# ==========================

def get_user_by_email(
    db: Session,
    email: str,
):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


# ==========================
# Get User By ID
# ==========================

def get_user_by_id(
    db: Session,
    user_id: int,
):

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )