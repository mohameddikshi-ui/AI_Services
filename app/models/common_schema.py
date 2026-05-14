from pydantic import BaseModel

from typing import List


# ==========================================
# AUTO INSIGHT ITEM
# ==========================================

class AutoInsightItemSchema(BaseModel):

    product_id: str

    product_name: str

    category: str | None = None

    total_orders: int

    insight_type: str

    priority: str

    trend_strength: str

    message: str

    recommendation: str


# ==========================================
# AUTO INSIGHTS RESPONSE
# ==========================================

class AutoInsightsResponseSchema(BaseModel):

    success: bool

    message: str

    page: int

    pageSize: int

    total_records: int

    total_pages: int

    data: List[AutoInsightItemSchema]