from fastapi import APIRouter, Query

from app.ai.qdrant_service import search

router = APIRouter(
    prefix="/semantic-search",
    tags=["AI Semantic Search"]
)


@router.get("/")
def semantic_search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(5, ge=1, le=20)
):
    """
    AI-powered semantic search.
    """

    results = search(
        query=q,
        limit=limit,
    )

    return {
        "query": q,
        "results": results,
        "count": len(results),
    }