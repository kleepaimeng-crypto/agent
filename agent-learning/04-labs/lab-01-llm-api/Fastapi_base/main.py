from fastapi import FastAPI

app = FastAPI()


@app.middleware("http")
async def middleware1(request, call_next):
    print("中间件1 start")

    response = await call_next(request)

    print("中间件1 end")
    return response


@app.get("/")
async def root():
    print("root 执行")
    return {"message": "Hello World"}