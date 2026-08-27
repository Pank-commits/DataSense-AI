from datetime import datetime

from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field


# ==========================
# Register Request
# ==========================

class UserRegister(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


# ==========================
# Login Request
# ==========================

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


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
