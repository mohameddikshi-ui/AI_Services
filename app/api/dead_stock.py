from fastapi import APIRouter, Query
from app.services.dead_stock_service import get_dead_stock

router = APIRouter(tags=["Dead Stock Analysis"])

@router.get("/dead-stock")
def dead_stock(
    page: int = 1,
    pageSize: int = 10,
    search: str = "",
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    return get_dead_stock(page, pageSize, search, start_date, end_date)