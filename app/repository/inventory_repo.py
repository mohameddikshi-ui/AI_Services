from sqlalchemy import text
from app.core.db import engine

def get_inventory_data(search, offset, limit):

    query = text("""
    SELECT 
        it.fItemcode,
        pd.FitemName,
        pd.Fimg1,
        c.fcate AS category,
        SUM(it.fTotQty) as total_sales

    FROM ItemTransaction it WITH (NOLOCK)

    JOIN ProductDetails pd 
        ON it.fItemcode = pd.Fitemcode

    LEFT JOIN category c 
        ON pd.FcategoryCode = c.Fcode

    WHERE pd.FitemName LIKE :search

    GROUP BY 
        it.fItemcode, 
        pd.FitemName, 
        pd.Fimg1,
        c.fcate

    ORDER BY total_sales DESC

    OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {
            "search": f"%{search}%",
            "offset": offset,
            "limit": limit
        })

        return [dict(row._mapping) for row in result]