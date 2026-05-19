from sqlalchemy import text

from app.core.db import engine


query = text("""

SELECT TOP 20

    pd.fItemcode,

    pd.fItemName,

    SUM(ISNULL(it.fTotQty, 0)) AS historical_sales,

    COUNT(DISTINCT CAST(it.fDate AS DATE)) AS active_days,

    CASE 
        WHEN COUNT(DISTINCT CAST(it.fDate AS DATE)) > 0
        THEN SUM(ISNULL(it.fTotQty, 0)) * 1.0 /
             COUNT(DISTINCT CAST(it.fDate AS DATE))
        ELSE 0
    END AS avg_daily_sales

FROM ItemTransaction it

INNER JOIN Item pd
    ON it.fItemcode = pd.fItemcode

WHERE

    DATENAME(MONTH, it.fDate) = :month

    AND YEAR(it.fDate) = :year

GROUP BY

    pd.fItemcode,

    pd.fItemName

HAVING SUM(ISNULL(it.fTotQty, 0)) > 0

ORDER BY historical_sales DESC

""")


params = {

    "month": "January",

    "year": 2026
}


with engine.connect() as conn:

    result = conn.execute(query, params)

    rows = result.fetchall()

    print("\n📌 INVENTORY MONTH TEST\n")

    print(f"Month : {params['month']}")

    print(f"Year  : {params['year']}\n")

    for row in rows:

        print(dict(row._mapping))