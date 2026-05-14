from app.repository.inventory_repo import get_inventory_data
from app.utils.pagination import get_pagination
from app.utils.calculations import (
    calculate_avg_daily,
    calculate_recommended
)
from app.utils.response import (
    success_response
)





def get_demand_level(avg):
    if avg > 2:
        return "HIGH"
    elif avg > 0.5:
        return "MEDIUM"
    return "LOW"


def calculate_inventory(page, pageSize, search):

    offset, limit = get_pagination(page, pageSize)

    data = get_inventory_data(search, offset, limit)

    result = []

    for item in data:
        total_sales = item.get("total_sales", 0)

        avg_daily = calculate_avg_daily(total_sales)
        recommended = calculate_recommended(avg_daily)

        image = item.get("Fimg1")
        image_url = image if image else None


        result.append({
            "product_id": item["fItemcode"],
            "product_name": item["FitemName"],
            "image": image_url,
            "category": item.get("category"),

            # 🔥 IMPORTANT CHANGE
            "current_stock": None,   # ❗ NOT 0

            "total_sales": total_sales,
            "avg_daily_sales": round(avg_daily, 3),
            "demand_level": get_demand_level(avg_daily),
            "recommended_stock": recommended
        })

    return success_response(
        message="Inventory data fetched successfully.",
        data=result,
        page=page,  
        total_records=len(result),
        pageSize=pageSize
    )   