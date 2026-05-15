from sqlalchemy import text
from app.core.db import engine


CATEGORY_CASE = """
CASE
    WHEN LTRIM(RTRIM(pd.fItemName)) LIKE 'G %' THEN 'Gold'
    WHEN LTRIM(RTRIM(pd.fItemName)) LIKE 'S %' THEN 'Silver'
    WHEN LTRIM(RTRIM(pd.fItemName)) LIKE 'D %' THEN 'Diamond'
    WHEN LTRIM(RTRIM(pd.fItemName)) LIKE 'DIAMOND%' THEN 'Diamond'
    WHEN LTRIM(RTRIM(pd.fItemName)) LIKE '%DIAMOND%' THEN 'Diamond'
    WHEN LTRIM(RTRIM(pd.fItemName)) LIKE 'N %' THEN 'Silver/Other'
    ELSE 'Other'
END
"""


def get_alert_data(search, offset, limit, filter_type="monthly", start_date=None, end_date=None):

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

        ISNULL(st.current_stock, 0) AS current_stock,

        SUM(ISNULL(it.fTotQty, 0)) AS recent_sales,

        COUNT(DISTINCT CAST(it.fDate AS DATE)) AS active_days,

        CASE 
            WHEN COUNT(DISTINCT CAST(it.fDate AS DATE)) > 0
            THEN SUM(ISNULL(it.fTotQty, 0)) * 1.0 / COUNT(DISTINCT CAST(it.fDate AS DATE))
            ELSE 0
        END AS avg_daily_sales

    FROM Item pd

    LEFT JOIN (
        SELECT
            Itemcode,
            SUM(ISNULL(Qty, 0)) AS current_stock
        FROM Stock
        WHERE Itemcode IS NOT NULL
        AND LTRIM(RTRIM(Itemcode)) <> ''
        GROUP BY Itemcode
    ) st
        ON pd.fItemcode = st.Itemcode

    LEFT JOIN ItemTransaction it
        ON pd.fItemcode = it.fItemcode
        {date_filter}
        {custom_date_filter}

    WHERE pd.fItemName LIKE :search
    AND pd.fItemcode IS NOT NULL
    AND LTRIM(RTRIM(pd.fItemcode)) <> ''

    GROUP BY
        pd.fItemcode,
        pd.fItemName,
        st.current_stock,
        {CATEGORY_CASE}

    ORDER BY recent_sales DESC

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