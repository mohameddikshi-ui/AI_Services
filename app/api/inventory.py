from fastapi import APIRouter

from datetime import date

from typing import Optional

from app.services.inventory_service import calculate_inventory

router = APIRouter(
    tags=["Inventory recommendation"]
)


@router.get("/inventory")
def get_inventory(

    page: int = 1,

    pageSize: int = 10,

    search: str = "",

    filter: str = "monthly",

    month: Optional[str] = None,

    year: Optional[int] = None,

    start_date: Optional[date] = None,

    end_date: Optional[date] = None
):

    return calculate_inventory(

        page,

        pageSize,

        search,

        filter,

        month,

        year,

        start_date,

        end_date
    )