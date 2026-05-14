from fastapi import APIRouter

from app.services.seasonal_service import analyze_seasonal_insights

router = APIRouter(tags=["Seasonal Insights"])


@router.get("/seasonal-insights")
def seasonal_insights(

    page: int = 1,

    pageSize: int = 10,

    month: str = ""
):

    return analyze_seasonal_insights(
        page,
        pageSize,
        month
    )