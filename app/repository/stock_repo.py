from sqlalchemy import text
from app.core.db import engine


def get_alert_data(search, offset, limit):

    query = text("""

    SELECT

        pd.Fitemcode,
        pd.FitemName,
        pd.Fimg1,

        c.fcate AS category,

        SUM(ISNULL(it.fTotQty, 0)) AS total_sales

    FROM ProductDetails pd

    LEFT JOIN ItemTransaction it
        ON pd.Fitemcode = it.fItemcode

    LEFT JOIN category c
        ON pd.FcategoryCode = c.Fcode

    WHERE pd.FitemName LIKE :search

    GROUP BY

        pd.Fitemcode,
        pd.FitemName,
        pd.Fimg1,
        c.fcate

    ORDER BY total_sales DESC

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