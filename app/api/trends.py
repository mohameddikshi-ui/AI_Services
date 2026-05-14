from fastapi import APIRouter, Query
from app.services.trend_service import get_trend_analysis

router = APIRouter(tags=["Trend Analysis"])


@router.get("/ai/trends")
def trends(
    page: int = Query(1),
    pageSize: int = Query(10),
    search: str = Query(""),
    filter: str = Query("monthly")
):
    return get_trend_analysis(page, pageSize, search, filter)