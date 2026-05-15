from sqlalchemy import text

from app.core.db import engine


query = text("""

SELECT TOP 20

    fItemcode,
    fItemName,
    fParent,
    fAclevel,
    fShow

FROM Item

WHERE fAclevel = -3

ORDER BY fItemcode

""")


with engine.connect() as conn:

    result = conn.execute(query)

    print("\n📌 SELLABLE ITEMS\n")

    for row in result:

        print(dict(row._mapping))