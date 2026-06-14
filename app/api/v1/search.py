from fastapi import APIRouter, Query
from app.services.ai_service import analyze_text

router = APIRouter(prefix="/search", tags=["Recherche"])

@router.get("")
async def search_errors(
    q: str = Query(..., min_length=2, description="Terme de recherche"),
    lang: str = Query("fr"),
    category: str = Query(None),
    severity: str = Query(None)
):
    result = await analyze_text(q, lang)
    return {
        "query": q,
        "results": [result],
        "total": 1
    }