"""
Authentication endpoint tests.
"""
from uuid import UUID

import pytest


class TestAuthEndpoints:
    """Test authentication endpoints."""

    async def test_health_check(self, client):
        """Test health check endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    async def test_register_success(self, client):
        """Test successful user registration."""
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "name": "Test User",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "userId" in data
        assert "token" in data
        assert "refreshToken" in data
        assert isinstance(UUID(data["userId"]), UUID)

    async def test_register_duplicate_email(self, client):
        """Test registration with duplicate email fails."""
        # First registration
        await client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "password123",
                "name": "User One",
            },
        )

        # Duplicate registration
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "password456",
                "name": "User Two",
            },
        )
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"]["error"]["message"]

    async def test_register_invalid_email(self, client):
        """Test registration with invalid email."""
        response = await client.post(
            "/api/auth/register",
            json={"email": "not-an-email", "password": "password123", "name": "Test"},
        )
        assert response.status_code == 422  # Validation error

    async def test_register_short_password(self, client):
        """Test registration with short password."""
        response = await client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "short", "name": "Test"},
        )
        assert response.status_code == 422

    async def test_login_success(self, client):
        """Test successful login."""
        # Register first
        await client.post(
            "/api/auth/register",
            json={
                "email": "login@example.com",
                "password": "password123",
                "name": "Login User",
            },
        )

        # Login
        response = await client.post(
            "/api/auth/login",
            json={"email": "login@example.com", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "userId" in data
        assert "token" in data

    async def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = await client.post(
            "/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "wrongpass"},
        )
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]["error"]["message"]
