from fastapi import APIRouter, Query
from app.services.top_selling_service import get_top_selling

router = APIRouter(tags=["Top Selling Products Analysis"])

@router.get("/top-selling")
def top_selling(
    page: int = 1,
    pageSize: int = 10,
    search: str = "",
    filter: str = "overall",
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    return get_top_selling(
        page,
        pageSize,
        search,
        filter,
        start_date,
        end_date
    )