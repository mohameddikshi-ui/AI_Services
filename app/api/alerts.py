from fastapi import APIRouter

from app.services.alert_service import get_smart_alerts

router = APIRouter(tags=["Smart Alerts"])


@router.get("/alerts")
def smart_alerts(

    page: int = 1,

    pageSize: int = 10,

    search: str = ""
):

    return get_smart_alerts(
        page,
        pageSize,
        search
    )