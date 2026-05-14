from fastapi import APIRouter

from app.services.auto_insights_service import (
    generate_auto_insights
)

from app.models.common_schema import (
    AutoInsightsResponseSchema
)

router = APIRouter(tags=["AI Auto Insights"])


@router.get(

    "/auto-insights",

    response_model=AutoInsightsResponseSchema
)
def auto_insights(

    page: int = 1,

    pageSize: int = 10
):

    return generate_auto_insights(
        page,
        pageSize
    )