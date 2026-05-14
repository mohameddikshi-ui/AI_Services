from fastapi import APIRouter
from datetime import date
from typing import Optional

from app.services.forecast_service import get_demand_forecast

router = APIRouter(tags=["Demand Forecasting"])


@router.get("/forecast")
def demand_forecast(
    page: int = 1,
    pageSize: int = 10,
    search: str = "",
    filter: str = "monthly",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    return get_demand_forecast(
        page,
        pageSize,
        search,
        filter,
        start_date,
        end_date
    )