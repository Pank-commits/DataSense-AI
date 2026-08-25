from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


# ==========================
# Register Request
# ==========================

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str


# ==========================
# Login Request
# ==========================

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ==========================
# User Response
# ==========================

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================
# Token Response
# ==========================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# ==========================
# Authentication Response
# ==========================

class AuthResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    user: UserResponse