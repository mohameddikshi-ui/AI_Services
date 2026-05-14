from app.repository.stock_repo import get_alert_data

from app.utils.pagination import (
    get_pagination
)

from app.utils.response import (
    success_response
)



def get_smart_alerts(page, pageSize, search):

    # ==========================================
    # PAGINATION
    # ==========================================

    offset, limit = get_pagination(
        page,
        pageSize
    )

    # ==========================================
    # FETCH DATA
    # ==========================================

    data = get_alert_data(
        search,
        offset,
        limit
    )

    result = []

    # ==========================================
    # PROCESS ALERTS
    # ==========================================

    for item in data:

        image = item.get("Fimg1")

        # ==========================================
        # IMAGE CLEANING
        # ==========================================

        if image:

            image = image.strip()

            image = image.replace(" ", "")

            image = image.replace("[", "")

            image = image.replace("]", "")

        image_url = image if image else None
    
        total_sales = float(
            item.get("total_sales") or 0
        )

        # ==========================================
        # AI ALERT ENGINE
        # ==========================================

        if total_sales >= 100:

            alert_type = "HIGH DEMAND"

            severity = "HIGH"

            recommendation = (
                "Restock immediately"
            )

        elif total_sales >= 40:

            alert_type = "FAST MOVING"

            severity = "MEDIUM"

            recommendation = (
                "Monitor inventory closely"
            )

        elif total_sales == 0:

            alert_type = "DEAD STOCK"

            severity = "HIGH"

            recommendation = (
                "Consider promotion or clearance"
            )

        else:

            alert_type = "NORMAL"

            severity = "LOW"

            recommendation = (
                "Stock level stable"
            )

        # ==========================================
        # FINAL ALERT OBJECT
        # ==========================================

        result.append({

            "product_id": item["Fitemcode"],

            "product_name": item["FitemName"],

            "image": image_url,

            "category": item.get("category"),

            "total_sales": total_sales,

            "alert_type": alert_type,

            "severity": severity,

            "recommendation": recommendation
        })

    # ==========================================
    # STANDARD RESPONSE
    # ==========================================

    return success_response(

        message=
        "Smart alerts fetched successfully.",

        data=result,

        page=page,

        pageSize=pageSize,

        total_records=len(result)
    )