from fastapi import APIRouter
from app.services.inventory_service import calculate_inventory


router = APIRouter(tags=["Inventory recommendation"])

@router.get("/inventory")
def get_inventory(page: int = 1, pageSize: int = 10, search: str = ""):
    return calculate_inventory(page, pageSize, search)