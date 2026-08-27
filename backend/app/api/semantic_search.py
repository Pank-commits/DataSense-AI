from fastapi import APIRouter, Query

from fastapi import APIRouter, HTTPException, Query
from app.ai.qdrant_service import search
from app.agents.dataset_agent import (
    understand_request,
    build_search_query,
    rerank_datasets,
)

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

    try:
        intent = understand_request(q)
        search_query = build_search_query(q, intent)
        results = search(query=search_query, limit=max(limit, 20), intent=intent)
        results = rerank_datasets(results, q, intent)[:limit]
    except Exception as error:
        raise HTTPException(status_code=503, detail="Semantic search is unavailable.") from error

    return {
        "query": q,
        "results": results,
        "count": len(results),
        "intent": intent,
    }
