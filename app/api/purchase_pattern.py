from fastapi import APIRouter

from app.services.pattern_service import analyze_purchase_patterns

router = APIRouter(tags=["Purchase Pattern Analysis"])


@router.get("/purchase-pattern")

def purchase_pattern(

    page: int = 1,

    pageSize: int = 10,

    search: str = "",

    filter: str = "overall",

    start_date: str = None,

    end_date: str = None
):

    return analyze_purchase_patterns(

        page,

        pageSize,

        search,

        filter,

        start_date,

        end_date
    )