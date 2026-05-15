from sqlalchemy import text

from app.core.db import engine


query = text("""

SELECT TOP 20

    s.Itemcode,

    i.fItemName,

    SUM(ISNULL(s.Qty, 0)) AS current_stock

FROM Stock s

INNER JOIN Item i
    ON s.Itemcode = i.fItemcode

WHERE s.Itemcode IS NOT NULL

GROUP BY

    s.Itemcode,

    i.fItemName

ORDER BY current_stock DESC

""")


with engine.connect() as conn:

    result = conn.execute(query)

    print("\n📌 CURRENT STOCK CHECK\n")

    for row in result:

        print(dict(row._mapping))