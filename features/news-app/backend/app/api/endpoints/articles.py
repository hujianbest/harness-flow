"""
Article endpoints.
"""
from typing import Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Query

from app.schemas import Article, ArticleListResponse, ArticleSource

router = APIRouter()

# Mock articles storage
mock_articles: list = []
mock_sources: list = [
    {"id": uuid4(), "name": "TechNews", "icon": "https://example.com/tech.png"},
    {"id": uuid4(), "name": "BusinessDaily", "icon": "https://example.com/biz.png"},
]


@router.get("", response_model=ArticleListResponse)
async def list_articles(
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    sourceId: Optional[UUID] = None,
    tag: Optional[str] = None,
    minQuality: int = Query(0, ge=0, le=5),
) -> ArticleListResponse:
    """
    Get article list with pagination and filtering.
    """
    # Filter articles
    filtered = mock_articles
    if sourceId:
        filtered = [a for a in filtered if a.get("sourceId") == sourceId]
    if tag:
        filtered = [a for a in filtered if tag in a.get("tags", [])]
    if minQuality > 0:
        filtered = [a for a in filtered if a.get("qualityScore", 0) >= minQuality]

    # Paginate
    total = len(filtered)
    start = (page - 1) * pageSize
    end = start + pageSize
    paginated = filtered[start:end]

    # Convert to response format
    articles = []
    for a in paginated:
        source = next((s for s in mock_sources if s["id"] == a.get("sourceId")), None)
        if source:
            articles.append(
                Article(
                    id=a["id"],
                    title=a["title"],
                    summary=a.get("summary"),
                    source=ArticleSource(
                        id=source["id"], name=source["name"], icon=source.get("icon")
                    ),
                    publishedAt=a.get("publishedAt"),
                    tags=a.get("tags", []),
                    readTime=a.get("readTime", 0),
                    qualityScore=a.get("qualityScore"),
                )
            )

    return ArticleListResponse(
        articles=articles, total=total, page=page, pageSize=pageSize
    )


@router.get("/{article_id}", response_model=Article)
async def get_article(article_id: UUID) -> Article:
    """
    Get article by ID.
    """
    article = next((a for a in mock_articles if a["id"] == article_id), None)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    source = next(
        (s for s in mock_sources if s["id"] == article.get("sourceId")), None
    )
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    return Article(
        id=article["id"],
        title=article["title"],
        summary=article.get("summary"),
        source=ArticleSource(
            id=source["id"], name=source["name"], icon=source.get("icon")
        ),
        publishedAt=article.get("publishedAt"),
        tags=article.get("tags", []),
        readTime=article.get("readTime", 0),
        qualityScore=article.get("qualityScore"),
    )
