from app.repository.sales_repo import get_category_performance

from app.utils.pagination import get_pagination
from app.utils.response import (
    success_response
)
    
def analyze_category_performance(page, pageSize, search, filter_type, start_date=None, end_date=None):

    offset, limit = get_pagination(page, pageSize)

    data = get_category_performance(
        search,
        offset,
        limit,
        filter_type,
        start_date,
        end_date
    )
    result = []

    for item in data:

        total_orders = int(item.get("total_orders") or 0)

        total_designs = int(item.get("total_designs") or 0)

        # 🔥 DESIGN DEMAND CLASSIFICATION
        if total_orders >= 1000:

            demand_level = "VERY HIGH"

        elif total_orders >= 500:

            demand_level = "HIGH"

        elif total_orders >= 100:

            demand_level = "MEDIUM"

        else:

            demand_level = "LOW"

        result.append({

            "category": item.get("category"),

            "total_designs": total_designs,

            "total_orders": total_orders,

            "demand_level": demand_level
        })

    return success_response(

        message="Category performance analysis fetched successfully.",

        data=result,

        page=page,

        pageSize=pageSize,
    
        total_records=len(result),

          extra={

        "filter": filter_type
    }
    )