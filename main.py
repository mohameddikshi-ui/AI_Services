from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.inventory import router as inventory_router
from app.api.top_selling import router as top_selling_router
from app.api.dead_stock import router as dead_stock_router
from app.api.trends import router as trends_router
from app.api.demand_forecast import router as forecast_router
from app.api.alerts import router as alerts_router
from app.api.purchase_pattern import router as purchase_pattern_router  
from app.api.category_performance import router as category_router
from app.api.seasonal_insights import router as seasonal_router
from app.api.auto_insights import router as auto_insights_router
from app.core.exceptions import (
    global_exception_handler
)   

app = FastAPI()
app.add_exception_handler(

    Exception,

    global_exception_handler
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory_router, prefix="/ai")
app.include_router(top_selling_router, prefix="/ai")
app.include_router(trends_router, prefix="/ai")
app.include_router(dead_stock_router, prefix="/ai")
app.include_router(forecast_router, prefix="/ai")
app.include_router(alerts_router, prefix="/ai")
app.include_router(purchase_pattern_router, prefix="/ai")
app.include_router(category_router, prefix="/ai")
app.include_router(seasonal_router, prefix="/ai")
app.include_router(auto_insights_router, prefix="/ai")
@app.get("/")
def home():
    return {"message": "AI Service Running 🚀"}