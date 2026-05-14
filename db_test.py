# from sqlalchemy import text
# from app.core.db import engine

# query = text("""

# SELECT TOP 20

#     pd.Fitemcode,
#     pd.FitemName,
#     c.fcate,
#     SUM(ISNULL(it.fTotQty, 0)) AS recent_sales

# FROM ProductDetails pd

# LEFT JOIN ItemTransaction it
#     ON pd.Fitemcode = it.fItemcode

# LEFT JOIN category c
#     ON pd.FcategoryCode = c.Fcode

# GROUP BY

#     pd.Fitemcode,
#     pd.FitemName,
#     c.fcate

# HAVING SUM(ISNULL(it.fTotQty, 0)) = 0

# ORDER BY pd.FitemName

# """)

# with engine.connect() as conn:

#     result = conn.execute(query)

#     print("\n📌 DEAD STOCK CHECK\n")

#     for row in result:

#         print(dict(row._mapping))