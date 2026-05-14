import os

from dotenv import load_dotenv

load_dotenv()


# ==========================================
# DATABASE
# ==========================================

DB_URL = os.getenv(
    "DB_URL"
)


