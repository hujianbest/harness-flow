"""
News source endpoints.
"""
from typing import Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Query

from app.schemas import Source, SourceCreate

router = APIRouter()

# Mock sources storage
mock_sources: list = [
    {
        "id": uuid4(),
        "name": "TechNews",
        "url": "https://technews.com/rss",
        "icon": "https://example.com/tech.png",
        "description": "Technology news aggregator",
        "isSystem": True,
        "isActive": True,
    },
    {
        "id": uuid4(),
        "name": "BusinessDaily",
        "url": "https://business.com/rss",
        "icon": "https://example.com/biz.png",
        "description": "Business and finance news",
        "isSystem": True,
        "isActive": True,
    },
]


@router.get("")
async def list_sources(
    isActive: Optional[bool] = None,
    isSystem: Optional[bool] = None,
) -> list[Source]:
    """
    Get list of news sources with optional filtering.
    """
    filtered = mock_sources

    if isActive is not None:
        filtered = [s for s in filtered if s.get("isActive") == isActive]
    if isSystem is not None:
        filtered = [s for s in filtered if s.get("isSystem") == isSystem]

    return [
        Source(
            id=s["id"],
            name=s["name"],
            url=s["url"],
            icon=s.get("icon"),
            description=s.get("description"),
            isSystem=s.get("isSystem", False),
            isActive=s.get("isActive", True),
        )
        for s in filtered
    ]


@router.post("", status_code=201)
async def create_source(source_data: SourceCreate) -> Source:
    """
    Add a custom RSS source.
    """
    # Check if URL already exists
    if any(s["url"] == source_data.url for s in mock_sources):
        raise HTTPException(status_code=409, detail="Source URL already exists")

    new_source = {
        "id": uuid4(),
        "name": source_data.name,
        "url": source_data.url,
        "icon": None,
        "description": None,
        "isSystem": False,
        "isActive": True,
    }
    mock_sources.append(new_source)

    return Source(
        id=new_source["id"],
        name=new_source["name"],
        url=new_source["url"],
        icon=new_source.get("icon"),
        description=new_source.get("description"),
        isSystem=new_source["isSystem"],
        isActive=new_source["isActive"],
    )


@router.delete("/{source_id}")
async def delete_source(source_id: UUID) -> dict:
    """
    Delete a custom news source.
    """
    source = next((s for s in mock_sources if s["id"] == source_id), None)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    if source.get("isSystem"):
        raise HTTPException(status_code=403, detail="Cannot delete system sources")

    mock_sources.remove(source)
    return {"message": "Source deleted successfully"}
