"""Schemas for Auth."""
from datetime import datetime
from pydantic import BaseModel, Field


class Token(BaseModel):
    """Schema for JWT token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for data stored in JWT token."""

    sub: str
    email: str
    name: str
    last_name: str
    exp: int | None = None


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    name: str = Field(..., description="User name")
    last_name: str = Field(..., description="User last name")
    email: str = Field(..., description="User e-mail address")
    password: str = Field(..., description="User password")


class UserRead(BaseModel):
    """Schema for reading a product record."""

    id: str = Field(..., description="ID of the user")
    name: str = Field(..., description="User name")
    last_name: str = Field(..., description="User last name")
    email: str = Field(..., description="User e-mail address")
