"""
Database models.
"""
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TimestampMixin:
    """Timestamp mixin for created_at and updated_at fields."""

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=True
    )


class User(Base, TimestampMixin):
    """User model."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    is_premium = Column(Boolean, default=False, nullable=False)
    email_verified_at = Column(DateTime, nullable=True)


class Source(Base, TimestampMixin):
    """News source model."""

    __tablename__ = "sources"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(500), unique=True, nullable=False)
    icon_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    fetch_interval = Column(Integer, default=3600, nullable=False)  # seconds
    last_fetched_at = Column(DateTime, nullable=True)
    fetch_error_count = Column(Integer, default=0, nullable=False)


class Article(Base, TimestampMixin):
    """Article model."""

    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True)
    source_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    url = Column(String(1000), unique=True, nullable=False)
    author = Column(String(100), nullable=True)
    published_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, nullable=False, server_default=func.now())

    # Quality scores
    quality_score = Column(Integer, nullable=True)  # 1-5
    quality_originality = Column(Float, nullable=True)
    quality_info_density = Column(Float, nullable=True)
    quality_accuracy = Column(Float, nullable=True)
    quality_readability = Column(Float, nullable=True)

    # Summary status
    summary_status = Column(String(20), default="pending", nullable=False)


class ArticleTag(Base):
    """Article tag association model."""

    __tablename__ = "article_tags"

    article_id = Column(UUID(as_uuid=True), primary_key=True)
    tag = Column(String(50), primary_key=True, nullable=False)


class ReadingHistory(Base, TimestampMixin):
    """Reading history model."""

    __tablename__ = "reading_history"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    article_id = Column(UUID(as_uuid=True), nullable=False)
    read_at = Column(DateTime, server_default=func.now(), nullable=False)
    read_duration = Column(Integer, nullable=True)  # seconds
    read_percentage = Column(Integer, nullable=True)  # 0-100
    is_completed = Column(Boolean, default=False, nullable=False)


class Favorite(Base):
    """Favorite model."""

    __tablename__ = "favorites"

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    article_id = Column(UUID(as_uuid=True), primary_key=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class UserTag(Base):
    """User interest tag model."""

    __tablename__ = "user_tags"

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    tag = Column(String(50), primary_key=True, nullable=False)
    weight = Column(Float, default=1.0, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
