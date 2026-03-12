from fastapi import APIRouter
from app.api.v1.api_health import router as health_router
from app.api.v1.api_wallets import router as wallets_router
from app.api.v1.api_operation import router as operation_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(wallets_router)
api_router.include_router(operation_router)
