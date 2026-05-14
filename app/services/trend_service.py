from app.repository.sales_repo import get_trend_data
from app.utils.pagination import get_pagination
from app.utils.response import success_response


def get_trend_analysis(page, pageSize, search, filter_type):

    offset, limit = get_pagination(page, pageSize)

    data = get_trend_data(search, offset, limit, filter_type)

    growing = []
    declining = []
    stable = []

    for item in data:

        current_sales = item.get("current_sales", 0) or 0
        previous_sales = item.get("previous_sales", 0) or 0

        if current_sales > previous_sales:
            trend = "GROWING"
        elif current_sales < previous_sales:
            trend = "DECLINING"
        else:
            trend = "STABLE"

        if previous_sales > 0:
            growth_percentage = round(
                ((current_sales - previous_sales) / previous_sales) * 100,
                2
            )
        elif current_sales > 0:
            growth_percentage = 100
        else:
            growth_percentage = 0

        product = {
            "product_id": item["Fitemcode"],
            "product_name": item["FitemName"],
            "category": item.get("category"),
            "current_sales": current_sales,
            "previous_sales": previous_sales,
            "growth_percentage": growth_percentage,
            "trend": trend
        }

        if trend == "GROWING":
            growing.append(product)
        elif trend == "DECLINING":
            declining.append(product)
        else:
            stable.append(product)

    return success_response(
        message="Trend analysis completed successfully.",
        data={
            "growing": growing,
            "declining": declining,
            "stable": stable
        },
        page=page,
        pageSize=pageSize,
        total_records=len(growing) + len(declining) + len(stable),
        extra={
            "filter": filter_type,
            "summary": {
                "growing_count": len(growing),
                "declining_count": len(declining),
                "stable_count": len(stable)
            }
        }
    )