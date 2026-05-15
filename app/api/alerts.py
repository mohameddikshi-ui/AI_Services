from fastapi import APIRouter
from datetime import date
from typing import Optional

from app.services.alert_service import get_smart_alerts

router = APIRouter(tags=["Smart Alerts"])


@router.get("/alerts")
def smart_alerts(
    page: int = 1,
    pageSize: int = 10,
    search: str = "",
    filter: str = "monthly",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    return get_smart_alerts(
        page,
        pageSize,
        search,
        filter,
        start_date,
        end_date
    )