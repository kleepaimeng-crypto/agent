from fastapi import APIRouter
from .item import item_router
from .user import user_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(user_router)
v1_router.include_router(item_router)