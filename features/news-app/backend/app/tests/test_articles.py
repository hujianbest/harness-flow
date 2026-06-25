"""
Article endpoint tests.
"""
import pytest


class TestArticleEndpoints:
    """Test article endpoints."""

    async def test_list_articles_default(self, client):
        """Test listing articles with default parameters."""
        response = await client.get("/api/articles")
        assert response.status_code == 200
        data = response.json()
        assert "articles" in data
        assert "total" in data
        assert "page" in data
        assert "pageSize" in data
        assert data["page"] == 1
        assert data["pageSize"] == 20

    async def test_list_articles_pagination(self, client):
        """Test article pagination."""
        response = await client.get("/api/articles?page=2&pageSize=10")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert data["pageSize"] == 10

    async def test_list_articles_filter_by_quality(self, client):
        """Test filtering articles by quality score."""
        response = await client.get("/api/articles?minQuality=4")
        assert response.status_code == 200
        # Verify all returned articles meet quality threshold
        data = response.json()
        for article in data["articles"]:
            if article.get("qualityScore") is not None:
                assert article["qualityScore"] >= 4

    async def test_list_articles_invalid_page(self, client):
        """Test with invalid page number."""
        response = await client.get("/api/articles?page=0")
        assert response.status_code == 422  # Validation error

    async def test_list_articles_invalid_page_size(self, client):
        """Test with invalid page size."""
        response = await client.get("/api/articles?pageSize=200")
        assert response.status_code == 422  # Max is 100


class TestSourceEndpoints:
    """Test news source endpoints."""

    async def test_list_sources_default(self, client):
        """Test listing sources."""
        response = await client.get("/api/sources")
        assert response.status_code == 200
        sources = response.json()
        assert isinstance(sources, list)
        assert len(sources) >= 2  # At least 2 mock sources

    async def test_list_sources_filter_active(self, client):
        """Test filtering active sources."""
        response = await client.get("/api/sources?isActive=true")
        assert response.status_code == 200
        sources = response.json()
        for source in sources:
            assert source["isActive"] is True

    async def test_list_sources_filter_system(self, client):
        """Test filtering system sources."""
        response = await client.get("/api/sources?isSystem=true")
        assert response.status_code == 200
        sources = response.json()
        for source in sources:
            assert source["isSystem"] is True

    async def test_create_custom_source(self, client):
        """Test creating a custom source."""
        response = await client.post(
            "/api/sources",
            json={"url": "https://custom.com/rss", "name": "Custom Feed"},
        )
        assert response.status_code == 201
        source = response.json()
        assert source["name"] == "Custom Feed"
        assert source["url"] == "https://custom.com/rss"
        assert source["isSystem"] is False

    async def test_create_duplicate_source(self, client):
        """Test creating source with duplicate URL."""
        # First attempt
        await client.post(
            "/api/sources",
            json={"url": "https://dup.com/rss", "name": "First"},
        )

        # Duplicate attempt
        response = await client.post(
            "/api/sources",
            json={"url": "https://dup.com/rss", "name": "Second"},
        )
        assert response.status_code == 409
