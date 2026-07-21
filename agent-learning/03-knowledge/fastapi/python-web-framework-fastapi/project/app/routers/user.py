from fastapi import APIRouter

user_router = APIRouter(tags=["user"], prefix="/user")

@user_router.get("say_hello")
async def say_hello():
    return "hello world"

@user_router.get("/say_hi")
async def say_hi():
    return "hi world"