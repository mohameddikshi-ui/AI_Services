from sqlalchemy import text
from app.core.db import engine


CATEGORY_CASE = """
CASE
    WHEN pd.fItemName LIKE 'G %' THEN 'Gold'
    WHEN pd.fItemName LIKE 'S %' THEN 'Silver'
    WHEN pd.fItemName LIKE 'D %' THEN 'Diamond'
    WHEN pd.fItemName LIKE 'N %' THEN 'Silver/Other'
    ELSE 'Other'
END
"""


def get_top_selling_data(search, offset, limit, filter_type, start_date=None, end_date=None):

    date_filter = ""
    custom_date_filter = ""

    if filter_type == "weekly":
        date_filter = "AND it.fDate >= DATEADD(DAY, -7, GETDATE())"
    elif filter_type == "monthly":
        date_filter = "AND it.fDate >= DATEADD(MONTH, -1, GETDATE())"

    if start_date and end_date:
        custom_date_filter = """
        AND it.fDate >= :start_date
        AND it.fDate < DATEADD(DAY, 1, :end_date)
        """

    query = text(f"""
    SELECT 
        it.fItemcode AS fItemcode,
        pd.fItemName AS FitemName,
        {CATEGORY_CASE} AS category,

        SUM(ISNULL(it.fTotQty, 0)) AS total_qty,
        SUM(ISNULL(it.fGms, 0)) AS total_weight,
        SUM(ISNULL(it.fAmount, 0)) AS total_sales

    FROM ItemTransaction it WITH (NOLOCK)

    JOIN Item pd 
        ON it.fItemcode = pd.fItemcode

    WHERE pd.fItemName LIKE :search
    {date_filter}
    {custom_date_filter}

    GROUP BY 
        it.fItemcode,
        pd.fItemName,
        {CATEGORY_CASE}

    ORDER BY SUM(ISNULL(it.fTotQty, 0)) DESC

    OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
    """)

    params = {
        "search": f"%{search}%",
        "offset": offset,
        "limit": limit
    }

    if start_date and end_date:
        params["start_date"] = start_date
        params["end_date"] = end_date

    with engine.connect() as conn:
        result = conn.execute(query, params)
        return [dict(row._mapping) for row in result]


def get_dead_stock_data(search, offset, limit, start_date=None, end_date=None):

    custom_date_filter = ""

    if start_date and end_date:
        custom_date_filter = """
        AND it.fDate >= :start_date
        AND it.fDate < DATEADD(DAY, 1, :end_date)
        """
    else:
        custom_date_filter = """
        AND it.fDate >= DATEADD(DAY, -30, GETDATE())
        """

    query = text(f"""
    SELECT 
        pd.fItemcode AS Fitemcode,
        pd.fItemName AS FitemName,
        {CATEGORY_CASE} AS category,

        SUM(CASE 
            WHEN it.fDate IS NOT NULL
            THEN ISNULL(it.fTotQty, 0)
            ELSE 0 
        END) AS recent_sales,

        CASE
            WHEN SUM(CASE 
                WHEN it.fDate IS NOT NULL
                THEN ISNULL(it.fTotQty, 0)
                ELSE 0 
            END) = 0
            THEN 'Dead Stock'
            ELSE 'Slow Moving'
        END AS stock_status

    FROM Item pd

    LEFT JOIN ItemTransaction it 
        ON pd.fItemcode = it.fItemcode
        {custom_date_filter}

    WHERE pd.fItemName LIKE :search
    AND pd.fItemcode IS NOT NULL
    AND LTRIM(RTRIM(pd.fItemcode)) <> ''
    AND pd.fItemName NOT LIKE '%GOLD%'
    AND pd.fItemName NOT LIKE '%SILVER%'
    AND pd.fItemName NOT LIKE '%OLD%'
    AND pd.fItemName NOT LIKE '%ROUND OFF%'
    AND pd.fItemName NOT LIKE '%CONVERSION%'

    GROUP BY 
        pd.fItemcode,
        pd.fItemName,
        {CATEGORY_CASE}

    HAVING 
        SUM(CASE 
            WHEN it.fDate IS NOT NULL
            THEN ISNULL(it.fTotQty, 0)
            ELSE 0 
        END) <= 5

    ORDER BY recent_sales ASC, pd.fItemName

    OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
    """)

    params = {
        "search": f"%{search}%",
        "offset": offset,
        "limit": limit
    }

    if start_date and end_date:
        params["start_date"] = start_date
        params["end_date"] = end_date

    with engine.connect() as conn:
        result = conn.execute(query, params)
        return [dict(row._mapping) for row in result]


def get_trend_data(search, offset, limit, filter_type):

    current_filter = ""
    previous_filter = ""

    if filter_type == "monthly":
        current_filter = "it.fDate >= DATEADD(MONTH, -1, GETDATE())"
        previous_filter = """
        it.fDate >= DATEADD(MONTH, -2, GETDATE())
        AND it.fDate < DATEADD(MONTH, -1, GETDATE())
        """

    elif filter_type == "weekly":
        current_filter = "it.fDate >= DATEADD(DAY, -7, GETDATE())"
        previous_filter = """
        it.fDate >= DATEADD(DAY, -14, GETDATE())
        AND it.fDate < DATEADD(DAY, -7, GETDATE())
        """

    else:
        current_filter = "1=1"
        previous_filter = "1=0"

    query = text(f"""
    SELECT
        pd.fItemcode AS Fitemcode,
        pd.fItemName AS FitemName,
        {CATEGORY_CASE} AS category,

        SUM(
            CASE
                WHEN {current_filter}
                THEN ISNULL(it.fTotQty, 0)
                ELSE 0
            END
        ) AS current_sales,

        SUM(
            CASE
                WHEN {previous_filter}
                THEN ISNULL(it.fTotQty, 0)
                ELSE 0
            END
        ) AS previous_sales

    FROM ItemTransaction it WITH (NOLOCK)

    JOIN Item pd
        ON it.fItemcode = pd.fItemcode

    WHERE pd.fItemName LIKE :search

    GROUP BY
        pd.fItemcode,
        pd.fItemName,
        {CATEGORY_CASE}

    ORDER BY current_sales DESC

    OFFSET :offset ROWS
    FETCH NEXT :limit ROWS ONLY
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {
            "search": f"%{search}%",
            "offset": offset,
            "limit": limit
        })

        return [dict(row._mapping) for row in result]


def get_forecast_data(search, offset, limit, filter_type, start_date=None, end_date=None):

    date_filter = ""
    custom_date_filter = ""

    if filter_type == "weekly":
        date_filter = "AND it.fDate >= DATEADD(DAY, -7, GETDATE())"

    elif filter_type == "monthly":
        date_filter = "AND it.fDate >= DATEADD(MONTH, -1, GETDATE())"

    if start_date and end_date:
        custom_date_filter = """
        AND it.fDate >= :start_date
        AND it.fDate < DATEADD(DAY, 1, :end_date)
        """

    query = text(f"""
    SELECT
        pd.fItemcode AS Fitemcode,
        pd.fItemName AS FitemName,
        {CATEGORY_CASE} AS category,

        SUM(ISNULL(it.fTotQty, 0)) AS total_sales,

        COUNT(DISTINCT CAST(it.fDate AS DATE)) AS active_days,

        CASE 
            WHEN COUNT(DISTINCT CAST(it.fDate AS DATE)) > 0
            THEN 
                SUM(ISNULL(it.fTotQty, 0)) * 1.0 / 
                COUNT(DISTINCT CAST(it.fDate AS DATE))
            ELSE 0
        END AS avg_sales

    FROM ItemTransaction it WITH (NOLOCK)

    JOIN Item pd
        ON it.fItemcode = pd.fItemcode

    WHERE pd.fItemName LIKE :search
    {date_filter}
    {custom_date_filter}

    GROUP BY
        pd.fItemcode,
        pd.fItemName,
        {CATEGORY_CASE}

    ORDER BY avg_sales DESC

    OFFSET :offset ROWS
    FETCH NEXT :limit ROWS ONLY
    """)

    params = {
        "search": f"%{search}%",
        "offset": offset,
        "limit": limit
    }

    if start_date and end_date:
        params["start_date"] = start_date
        params["end_date"] = end_date

    with engine.connect() as conn:
        result = conn.execute(query, params)
        return [dict(row._mapping) for row in result]


def get_purchase_patterns(search, offset, limit):
    return []

def get_category_performance(search, offset, limit, filter_type, start_date=None, end_date=None):

    date_filter = ""
    custom_date_filter = ""

    if filter_type == "weekly":
        date_filter = "AND it.fDate >= DATEADD(DAY, -7, GETDATE())"

    elif filter_type == "monthly":
        date_filter = "AND it.fDate >= DATEADD(MONTH, -1, GETDATE())"

    if start_date and end_date:
        custom_date_filter = """
        AND it.fDate >= :start_date
        AND it.fDate < DATEADD(DAY, 1, :end_date)
        """

    query = text(f"""
    SELECT
        {CATEGORY_CASE} AS category,

        COUNT(DISTINCT pd.fItemcode) AS total_designs,

        SUM(ISNULL(it.fTotQty, 0)) AS total_orders

    FROM ItemTransaction it WITH (NOLOCK)

    JOIN Item pd
        ON it.fItemcode = pd.fItemcode

    WHERE pd.fItemName LIKE :search
    {date_filter}
    {custom_date_filter}

    GROUP BY
        {CATEGORY_CASE}

    ORDER BY total_orders DESC

    OFFSET :offset ROWS
    FETCH NEXT :limit ROWS ONLY
    """)

    params = {
        "search": f"%{search}%",
        "offset": offset,
        "limit": limit
    }

    if start_date and end_date:
        params["start_date"] = start_date
        params["end_date"] = end_date

    with engine.connect() as conn:
        result = conn.execute(query, params)
        return [dict(row._mapping) for row in result]

def get_seasonal_insights(month, offset, limit):
    return []


def get_auto_insights_data(offset, limit):
    return {
        "records": [],
        "total_records": 0
    }