from app.repository.sales_repo import get_seasonal_insights

from app.utils.pagination import get_pagination

from app.utils.response import (
    success_response
)


def analyze_seasonal_insights(
    page,
    pageSize,
    month
):

    # ==========================================
    # PAGINATION
    # ==========================================

    offset, limit = get_pagination(
        page,
        pageSize
    )

    # ==========================================
    # FETCH DB DATA
    # ==========================================

    data = get_seasonal_insights(
        month,
        offset,
        limit
    )

    result = []

    # ==========================================
    # AI SEASONAL ANALYSIS
    # ==========================================

    for item in data:

        total_orders = int(
            item.get("total_orders") or 0
        )

        # ==========================================
        # SEASONAL TREND CLASSIFICATION
        # ==========================================

        if total_orders >= 1000:

            seasonal_trend = "PEAK DEMAND"

            data_confidence = "HIGH"

        elif total_orders >= 500:

            seasonal_trend = "HIGH DEMAND"

            data_confidence = "HIGH"

        elif total_orders >= 100:

            seasonal_trend = "MODERATE DEMAND"

            data_confidence = "MEDIUM"

        else:

            seasonal_trend = "LOW DEMAND"

            data_confidence = "LOW"

        # ==========================================
        # FINAL OBJECT
        # ==========================================

        result.append({

            "month": item.get("month_name"),

            "category": item.get("category"),

            "total_orders": total_orders,

            "seasonal_trend": seasonal_trend,

            "data_confidence": data_confidence
        })

    # ==========================================
    # FINAL RESPONSE
    # ==========================================

    return success_response(

        message=
        "Seasonal insights analyzed successfully.",

        data=result,

        page=page,

        pageSize=pageSize,

        total_records=len(result),

       extra={

        "month": month
    }
    )