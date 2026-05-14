from sqlalchemy import create_engine
from app.core.config import DB_URL

engine = create_engine(
    DB_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)