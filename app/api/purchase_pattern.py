from fastapi import APIRouter

from app.services.pattern_service import analyze_purchase_patterns

router = APIRouter(tags=["Purchase Pattern Analysis"])


@router.get("/purchase-pattern")
def purchase_patterns(

    page: int = 1,

    pageSize: int = 10,

    search: str = ""
):

    return analyze_purchase_patterns(
        page,
        pageSize,
        search
    )