from fastapi import APIRouter

from api.routers import v1

registed_routers = APIRouter()

registed_routers.include_router(v1.router, tags=["PREDICT"])