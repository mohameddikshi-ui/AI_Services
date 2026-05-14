from fastapi import APIRouter
from datetime import date
from typing import Optional
from app.services.category_service import analyze_category_performance

router = APIRouter(tags=["Category Performance Analysis"])


@router.get("/category-performance")
def category_performance(

    page: int = 1,

    pageSize: int = 10,

    search: str = "",

    filter: str = "overall",

    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):

    return analyze_category_performance(
        page,
        pageSize,
        search,
        filter,
        start_date,
        end_date
    )