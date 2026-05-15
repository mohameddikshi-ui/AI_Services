from app.repository.sales_repo import get_purchase_patterns

from app.utils.pagination import get_pagination

from app.utils.response import (
    success_response
)


def analyze_purchase_patterns(

    page,

    pageSize,

    search,

    filter_type,

    start_date=None,

    end_date=None
):

    offset, limit = get_pagination(
        page,
        pageSize
    )

    data = get_purchase_patterns(

        search,

        offset,

        limit,

        filter_type,

        start_date,

        end_date
    )

    result = []

    for item in data:

        pair_count = int(
            item.get("pair_count") or 0
        )

        # ==========================================
        # AI ASSOCIATION STRENGTH
        # ==========================================

        if pair_count >= 100:

            strength = "VERY HIGH"

        elif pair_count >= 50:

            strength = "HIGH"

        elif pair_count >= 20:

            strength = "MEDIUM"

        else:

            strength = "LOW"

        result.append({

            "primary_product":
            item["primary_product"],

            "frequently_bought_with":
            item["paired_product"],

            "pair_count":
            pair_count,

            "strength":
            strength
        })

    return success_response(

        message=
        "Purchase patterns analyzed successfully.",

        data=result,

        page=page,

        pageSize=pageSize,

        total_records=len(result),

        extra={

            "filter": filter_type,

            "start_date": start_date,

            "end_date": end_date
        }
    )