from fastapi import APIRouter

item_router = APIRouter(tags=["items"], prefix="/items")

@item_router.get("/say_hello")
async def say_hello():
    return "hello world"

@item_router.get("/say_hi")
async def say_hi():
    return "hi world"