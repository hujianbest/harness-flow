"""
Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# Auth Schemas
class UserRegister(BaseModel):
    """User registration schema."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)
    name: str = Field(..., min_length=1, max_length=50)


class UserLogin(BaseModel):
    """User login schema."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""

    userId: UUID
    token: str
    refreshToken: str


# Article Schemas
class ArticleSource(BaseModel):
    """Article source in article response."""

    id: UUID
    name: str
    icon: Optional[str] = None


class Article(BaseModel):
    """Article response schema."""

    id: UUID
    title: str
    summary: Optional[str] = None
    source: ArticleSource
    publishedAt: Optional[datetime] = None
    tags: list[str] = []
    readTime: int = 0
    qualityScore: Optional[int] = None


class ArticleListResponse(BaseModel):
    """Article list response schema."""

    articles: list[Article]
    total: int
    page: int
    pageSize: int


# Source Schemas
class Source(BaseModel):
    """Source response schema."""

    id: UUID
    name: str
    url: str
    icon: Optional[str] = None
    description: Optional[str] = None
    isSystem: bool = False
    isActive: bool = True


class SourceCreate(BaseModel):
    """Source creation schema."""

    url: str
    name: str = Field(..., min_length=1, max_length=100)


# Common Schemas
class ErrorDetail(BaseModel):
    """Error detail schema."""

    field: Optional[str] = None
    issue: str


class ErrorResponse(BaseModel):
    """Error response schema."""

    error: dict
    requestId: Optional[str] = None


# User Schemas
class UserResponse(BaseModel):
    """User response schema."""

    id: UUID
    email: EmailStr
    name: str
    avatarUrl: Optional[str] = None
    isPremium: bool = False
