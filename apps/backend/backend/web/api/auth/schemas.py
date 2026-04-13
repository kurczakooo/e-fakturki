"""Schemas for Auth."""

from datetime import datetime, timedelta

from pydantic import BaseModel, Field


class Token(BaseModel):
    """Schema for JWT token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for data stored in JWT token."""

    sub: int
    email: str
    name: str
    last_name: str
    exp: timedelta | None = None


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    name: str = Field(..., description="User name")
    last_name: str = Field(..., description="User last name")
    email: str = Field(..., description="User e-mail address")
    password: str = Field(..., description="User password")


class UserRead(UserCreate):
    """Schema for reading a product record."""

    id: int = Field(..., description="ID of the user")
    is_active: bool = Field(..., description="Whether the user account is active")
    created_at: datetime = Field(
        ..., description="Timestamp of when the user was created"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp of when the user was last updated"
    )

    class Config:
        from_attributes = True
