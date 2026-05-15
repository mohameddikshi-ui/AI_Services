from fastapi import APIRouter

from app.services.auto_insights_service import (
    generate_auto_insights
)

router = APIRouter(
    tags=["AI Auto Insights"]
)


@router.get("/auto-insights")

def auto_insights(

    page: int = 1,

    pageSize: int = 10,

    filter: str = "overall",

    start_date: str = None,

    end_date: str = None
):

    return generate_auto_insights(

        page,

        pageSize,

        filter,

        start_date,

        end_date
    )