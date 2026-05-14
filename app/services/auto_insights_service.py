import math

from app.repository.sales_repo import (
    get_auto_insights_data
)

from app.utils.pagination import (
    get_pagination
)

from app.utils.response import (
    success_response
)

from app.constants.thresholds import (

    HIGH_DEMAND_PERCENTILE,

    MEDIUM_DEMAND_PERCENTILE
)


def generate_auto_insights(page, pageSize):

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

    db_data = get_auto_insights_data(
        offset,
        limit
    )

    data = db_data["records"]

    total_records = db_data["total_records"]

    # ==========================================
    # AI DYNAMIC ANALYTICS
    # ==========================================

    order_values = [

        int(item.get("total_orders") or 0)

        for item in data
    ]

    max_orders = max(order_values) if order_values else 0

    insights = []

    # ==========================================
    # INSIGHT GENERATION
    # ==========================================

    for item in data:

        total_orders = int(
            item.get("total_orders") or 0
        )

        product_id = item.get("Fitemcode")

        product_name = item.get("FitemName")

        category = item.get("category")

        # ==========================================
        # DYNAMIC DEMAND SCORE
        # ==========================================

        demand_score = 0

        if max_orders > 0:

            demand_score = round(
                (total_orders / max_orders) * 100,
                2
            )

        # ==========================================
        # AI DEMAND CLASSIFICATION
        # ==========================================

        if demand_score >= HIGH_DEMAND_PERCENTILE:

            insight_type = "HIGH DEMAND"

            priority = "HIGH"

            trend_strength = "HIGH"

            message = (
                f"{product_name} is showing exceptional customer demand."
            )

            recommendation = (
                "Increase production planning and prioritize design visibility."
            )

        elif demand_score >= MEDIUM_DEMAND_PERCENTILE:

            insight_type = "STABLE DEMAND"

            priority = "MEDIUM"

            trend_strength = "MEDIUM"

            message = (
                f"{product_name} maintains consistent order movement."
            )

            recommendation = (
                "Maintain regular production levels and monitor trends."
            )

        else:

            insight_type = "LOW DEMAND"

            priority = "LOW"

            trend_strength = "LOW"

            message = (
                f"{product_name} has relatively lower customer movement."
            )

            recommendation = (
                "Consider promotional visibility or refresh product exposure."
            )

        # ==========================================
        # FINAL INSIGHT OBJECT
        # ==========================================

        insights.append({

            "product_id": product_id,

            "product_name": product_name,

            "category": category,

            "total_orders": total_orders,

            "demand_score": demand_score,

            "insight_type": insight_type,

            "priority": priority,

            "trend_strength": trend_strength,

            "message": message,

            "recommendation": recommendation
        })

    # ==========================================
    # FINAL STANDARD RESPONSE
    # ==========================================

    return success_response(

        message=
        "AI auto insights fetched successfully.",

        data=insights,

        page=page,

        pageSize=pageSize,

        total_records=total_records
    )