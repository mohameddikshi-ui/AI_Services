from app.repository.sales_repo import get_dead_stock_data
from app.utils.pagination import get_pagination
from app.utils.response import success_response


def get_dead_stock(page, pageSize, search, start_date=None, end_date=None):

    offset, limit = get_pagination(page, pageSize)

    data = get_dead_stock_data(
        search,
        offset,
        limit,
        start_date,
        end_date
    )

    result = []

    for item in data:
        result.append({
            "product_id": item["Fitemcode"],
            "product_name": item["FitemName"],
            "category": item.get("category"),
            "recent_sales": item.get("recent_sales", 0),
            "status": item.get("stock_status", "Dead Stock")
        })

    return success_response(
        message="Dead / slow moving stock data fetched successfully.",
        data=result,
        page=page,
        total_records=len(result),
        pageSize=pageSize
    )