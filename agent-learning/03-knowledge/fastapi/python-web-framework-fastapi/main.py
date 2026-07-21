"""
# 创建虚拟环境：.venv 隔离项目运行环境，避免依赖冲突，保持全局环境的干净和稳定
# 启动fastapi应用命令：  uvicorn main:app --reload
# uvicorn - ASGI 高性能服务器，用于运行 FastAPI 应用
"""

from fastapi import FastAPI, Path, Query, HTTPException, Depends, Header, status, APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field

import time
import asyncio
# ----------------------------全局级别依赖注入----------
# 依赖函数：对所有API记录请求信息
async def log_request(request: Request):
    print(f"Request received: {request.method}%s{request.url}" % " ")
    print(f"Request Header: {request.headers}%s{type(request.headers)}" % " ")
    return {"logged": True}
app = FastAPI(dependencies=[Depends(log_request)])


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 路由是URL地址和处理函数之间的映射关系  @app是FastAPI的实例
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/user_test/hello")
async def hello():
    return {"msg": "我正在学习FastAPI...."}


@app.get("/hello")
async def get_hello():
    return {"msg": "你好 FastAPI"}


# --------------------------------------------同步和异步-------------------------
# 异步
@app.get("/async")
async def func_async():
    # 开始时间
    start = time.time()
    # 异步执行10个任务：单个任务耗时1sec
    tasks = [asyncio.sleep(1) for i in range(1000)]
    await asyncio.gather(*tasks)
    end = time.time()
    return {"time": f"{end - start:.2f}sec"}


# 同步
@app.get("/sync")
def func_sync():
    start = time.time()
    # 同步执行10个任务：单个任务耗时1sec
    for i in range(10):
        time.sleep(1)
    end = time.time()
    return {"time": f"{end - start:.2f}sec"}


# ------------------------------路径参数、查询参数、请求体参数----------------------

# 路径参数    路径参数传到处理函数的形参中   id: int 参数类型注解
@app.get("/test_book/{id}")  # ...表示必填，gt大于，lt小于，description描述
async def get_book(id: int = Path(..., gt=0, lt=102, descripion='书籍id，取值范围【1-101】')):
    return {
        "id": id,
        "title": f"这是第{id}本书"
    }


# 需求：查找书籍的作者，路径参数 name，长度范围2-10
@app.get("/author/{name}")  # Path(...)
async def get_name(name: str = Path(..., min_length=2, max_length=10)):
    return {"msg": f"这是{name}作者的信息"}


@app.get("user_test/{user_id}")
async def get_user_info(user_id: int):
    return {
        "user_id": user_id,
        "name": user_id
    }


# 以新闻分类id为参数设计URL，id范围为1~100
@app.get("/news/id/{news_category_id}")
async def get_news(news_category_id: int = Path(..., gt=0, lt=101)):
    return {
        "news_category_id": news_category_id,
        "title": f"这是第{news_category_id}条新闻"
    }


# 需求：以新闻分类名称为参数设计URL，名称长度范围2-10
@app.get("/news/name/{category_name}")
async def get_news_category(category_name: str = Path(..., min_length=2, max_length=10)):
    return {
        "category_name": category_name,
        "title": f"这是{category_name}分类下的新闻"
    }


# ---------------------------查询参数 URL?k=v&k=v ---------------------------------
# 固定路径应放在动态路径之前。例如：/news/news_list 应该放在/news/{category_id}之前。否则：/news/news_list中的news_list会被匹配到/news/{category_id},然后报类型错误
# 需求 查询新闻 -> 分页，skip：跳过的记录数， limit：返回的记录数 10
@app.get("/news/list/news_list")
async def get_news_list(
        skip: int = Query(0, description="跳过的记录数", lt=100),
        limit: int = Query(10, description="返回的记录数")
):  # 默认就是查询参数 URL?k=v&k=v
    return {
        "skip": skip,
        "limit": limit
    }


@app.get("/test_book/get_book")
async def get_book_list(
        book_category_name: str = Query("Python开发", min_length=5, max_length=255),
        book_price: int = Query(ge=50, le=100)
):
    # 响应类型 - JSON格式
    return {
        "book_category_name": book_category_name,
        "book_price": book_price
    }


# ---------------------------请求体参数，通常使用pydantic的BaseModel和Field进行数据校验---------------------------------
class User(BaseModel):
    username: str = Field(default="张三", min_length=2, max_length=10, description="用户名，长度要求2-10个字符")
    password: str = Field(min_length=3, max_length=20)


# 需求：注册用户
@app.post("/user_test/register")
async def register(user: User):
    return user


# Field(default="") 没有default默认值。...表示必填
class MyBook(BaseModel):
    name: str = Field(..., min_length=2, max_length=20)  # 书名
    author: str = Field(..., min_length=2, max_length=10)  # 作者
    publisher: str = Field(default="黑马程序员")  # 出版社
    sell_price: float = Field(..., gt=0)  # 销售价格


# 需求：新增图书
@app.post("/test_book/create")
async def create_book(book: MyBook):
    return book


# ----------------响应类型-JSON格式 | HTML格式：HTMLResponse------------------
# 在装饰器中添加response_class参数，指定响应类型：HTMLResponse
@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return """
    <html>
        <body>
            <h1>这是HTML格式的响应</h1>
        </body>
    </html>
    """


# ------------------------响应类型-文件下载：FileResponse------------------
# 接口：返回文件
@app.get("/file")
async def get_file():
    path = "./assets/img.png"
    return FileResponse(path)


# ------------------------响应类型-自定义响应数据格式，基于Pydantic的BaseModel。response_model=News------------------
# 需求：新闻接口 -> 响应数据格式 id、title、content。跟请求体参数一样，少了Field类型注解
class News(BaseModel):
    id: int
    title: str
    content: str


# 路径参数
@app.get("/news/{id}", response_model=News)
async def get_new(id: int):
    return {
        "id": id,
        "title": f"这是第{id}条新闻",
        "content": f"这是第{id}条新闻的内容啊多发点沙发沙发"
    }


# ------------------异常处理 raise HTTPException(status_code=404, detail="报错了，xxx") ----------------------------
# 需求：根据id查询新闻 -> 1-6
@app.get("/news/httpexception/{id}")
async def get_news(id: int):
    id_list = [1, 2, 3, 4, 5, 6]
    if id not in id_list:
        raise HTTPException(status_code=404, detail="你查找的新闻不存在")
    return {"id": id, "title": f"这是第{id}条新闻"}


# ------------------中间件，自定义中间件要处理的逻辑。这里只是简单的使用print前后。实际过程可以记录请求体的请求参数请求头请求api等请求信息，也可以记录response服务器返回的数据或者报错信息----------------------------
# async 代表异步函数。真有异步代码await要带上。
@app.middleware("http")
async def middleware(request, call_next):  # request是请求，call_next是传递请求的函数名
    print("中间件1开始处理  --  start")
    response = await call_next(request)  # 这里就有异步代码
    print("中间件1处理完成 -- end")
    return response


# async 代表异步函数。异步代码中，要用await让协程等待call_next函数返回结果，然后协程才继续往下走
@app.middleware("http")
async def middleware(request, call_next):
    print("中间件2开始处理  --  start")
    response = await call_next(request)
    print("中间件2处理完成 -- end")
    return response


# 多个中间件的输出顺序：类似于栈的先进后出
# 中间件2开始处理  --  start
# 中间件1开始处理  --  start
# 中间件1处理完成 -- end
# 中间件2处理完成 -- end


# -----------------------16_依赖注入 Depends() ---------------------------
# 需求：分页参数逻辑共用：新闻列表和用户列表      16-1.定义依赖项(分页的请求参数共用）
async def common_parameters(
        skip: int = Query(0, ge=0),  # skip跳过 >= 0
        limit: int = Query(10, le=60)  # page_size默认值10，范围0-60
):
    return {"skip": skip, "limit": limit}


# 查询参数 URL?k=v&k=v       ； 16-2.声明依赖项commons=Depends(common_parameters)
@app.get("/news_16/news_list")
async def get_news_list(commons=Depends(common_parameters)):
    return commons


# 查询参数 URL?k=v&k=v      ；声明依赖项commons=Depends(common_parameters)
@app.get("/user_16/user_list")
async def get_user_list(commons=Depends(common_parameters)):
    return commons


# ---------------------------------路径级依赖注入--------------------------------

# 依赖函数：检查用户权限
def check_user_permission(authorization: str = Header(...)):
    """
    检查用户权限的依赖函数
    支持 Authorization: Bearer <token> 格式
    """
    # 提取 Bearer token 中的实际 token 值
    token=""
    if authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]  # 获取 "Bearer" 后面的实际 token
    else:
        # 如果不是 Bearer 格式，直接使用整个值
        token = authorization

    # 验证 token
    if token != "secret-token":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

    return {"user": "admin"}


# 路径级依赖注入
@app.get("/admin", dependencies=[Depends(check_user_permission)])
async def admin_dashboard():
    return {"message": "Hello, admin"}


# ----------------------------------------路由级依赖-------------------------
# 依赖函数：检查用户权限
def check_auth(token: str = Header()):
    if token != "secret-token":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    return {"user": "admin"}

# 路由级依赖,用户验证token才能访问的api
router = APIRouter(dependencies=[Depends(check_auth)])

@router.get("/admin/dashboard")
async def admin_dashboard():
    return {"message": "Hello, admin"}

@router.get("/admin/users")
async def list_users():
    return {"users": ["user1", "user2", "user3"]}
app.include_router(router)


# --------------------嵌套依赖-------------------------------
# 验证token是否合法。    Http请求头里面拿到authorization
async def verify_token(authorization: str = Header(...)):
    """
        检查用户权限的依赖函数
        支持 Authorization: Bearer <token> 格式
        """
    # 提取 Bearer token 中的实际 token 值
    token = ""
    if authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]  # 获取 "Bearer" 后面的实际 token
    else:
        # 如果不是 Bearer 格式，直接使用整个值
        token = authorization

    # 验证 token
    if token != "secret-token":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    return token

# 根据token获取当前用户信息
async def get_current_user(token: str = Depends(verify_token)):
    return {"user": "admin", "token": token}

# 获取当前用户信息
@app.get("/user/get_current_user_info")
async def get_current_user_info(user: dict = Depends(get_current_user)):
    """
    获取当前用户信息
    :param user: 字典。
    :return:
    """
    return user

# ------------------------- 18_ORM安装和建表 -----------------------
# pip install sqlalchemy       优秀的ORM框架
# pip install aiomysql

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func, DateTime, String, Float, select

# 1. 创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/fastapi_first?charset=utf8"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # 可选，输出SQL日志
    pool_size=10,  # 设置连接池活跃的连接数
    max_overflow=20,  # 允许额外的连接数
)


# 2. 定义模型类： 基类 + 表对应的模型类
# 基类：创建时间、更新时间；书籍表：id、书名、作者、价格、出版社
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now(),
                                                  comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now(),
                                                  onupdate=func.now(), comment="更新时间", )


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str] = mapped_column(String(255), comment="出版社")


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, comment="用户id")
    username: Mapped[str] = mapped_column(String(255), comment="用户名")
    password: Mapped[str] = mapped_column(String(255), comment="密码")


# 3. 建表：定义函数建表   FastAPI启动时候调用建表的函数
async def create_tables():
    # 获取异步引擎，创建事务  - 建表             as 别名。。。async with  异步上下文管理器。
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # 继承了Base模型类的元数据（表），都会被创建


# app启动时候，创建表。真实开发：是直接根据DDL sql语句把表结构创建好。
@app.on_event("startup")
async def startup_event():
    await create_tables()


# -------------------------- 19_在路由中使用ORM -----------------------
# 需求：查询功能的接口，查询图书 。依赖注入：创建依赖项获取数据库会话 + Depends 注入路由处理函数
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定会话类
    expire_on_commit=False  # 提交后会话不过期，不会重新查询数据库
)


# 依赖项：获取数据库会话
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 返回数据库会话给路由处理函数
            await session.commit()  # 提交事务
        except Exception:
            await session.rollback()  # 有异常，回滚
            raise
        finally:
            await session.close()  # 关闭会话


# -----------------------20_ORM查询数据------------------------------
@app.get("/book/get_books")
async def get_book_list(db: AsyncSession = Depends(get_database)):
    # # 查询书籍列表     看下依赖有没有注入成功。注入数据库会话
    # result = await db.execute(select(Book))     # 查询 返回一个ORM对象
    # books = result.scalars().all()      # 获取所有书籍
    # book = result.scalars().first()     # 获取第一条数据
    book = await db.get(Book, 2)  # 根据id主键获取单条数据
    return book


# -----------------------21_OR查询数据。条件查询--比较判断----------------
# 需求：路径参数：数据ID        比较判断
@app.get("/book/book_detail/{book_id}")
async def get_book_detail(book_id: int, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    # 假设用户传递的数据ID不存在，所以返回None
    book_detail = result.scalar_one_or_none()
    return book_detail


# 需求：条件查询 价格大于等于30        比较判断
@app.get("/book/search_book_by_operation")
async def search_book_by_operation(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.price >= 30))
    books = result.scalars().all()
    return books


# ---------------22_ORM查询数据 条件查询-模糊查询&与非&包含----------------
# 需求 ：作者以 曹开头 %
@app.get("/book/search_book_by_author_like")
async def search_book_by_author_like(db: AsyncSession = Depends(get_database)):
    # where(Book.column.like("value%"))  1.模糊查询
    # result = await db.execute(select(Book).where(Book.author.like("曹%")))
    # result = await db.execute(select(Book).where(Book.author.like("曹_")))

    # 2. where( (条件1) & (条件2) )  与 【and & ,都行】            where( (条件1) | (条件2) )  或         where( ~(条件) )  非
    # result = await db.execute(select(Book).where(~(Book.author.like("曹%")) | (Book.price >= 20)))
    # result = await db.execute(select(Book).where(Book.author.like("曹%"),Book.price >= 20))

    # 3. 需求：书籍id列表，数据库里面的id如果在书籍id列表里面，就返回能查询得到的
    id_list = [1, 2, 4, 999]
    result = await db.execute(select(Book).where(Book.id.in_(id_list)))
    books = result.scalars().all()
    return books


# -------------------23,ORM查询数据，聚合查询 min,max,avg,--------------------------
@app.get("/book/count")
async def get_count(db: AsyncSession = Depends(get_database)):
    # result=  await db.execute(select(func.max(Book.price)))
    # result=  await db.execute(select(func.min(Book.price)))
    # result = await db.execute(select(func.avg(Book.price)))
    # 计算多少行
    result =  await db.execute(select(func.count(Book.id)))
    return result.scalar()  # 用来提取一个数据 = > 标量值


# --------------------24，ORM数据库操作，ORM分页炒作---------------------
@app.get("/book/get_book_page_list")
async def get_book_page_list(
        page: int = 2,
        page_size: int = 2,
        db: AsyncSession = Depends(get_database)
):
    # offset = (page - 1) * page_size   跳过的记录数；limit 每页的记录数
    offset = page_size * (page - 1)
    stmt = select(Book).offset(offset).limit(page_size)
    result = await db.execute(stmt)
    books = result.scalars().all()
    return books


# ----------------- 26,ORM操作数据，添加数据--------------------------
# 需求：用户输入图书信息（id、书名、作者、价格、出版社）。使用HTTP请求体传递用户输入数据
class BookCreate(BaseModel):  # 使用pydantic的BaseModel对输入的数据进行校验
    id: int
    bookname: str
    author: str
    price: float
    publisher: str


# 新增图书
@app.post("/book/add_book")
async def add_book(book: BookCreate, db: AsyncSession = Depends(get_database)):
    # ORM对象   -- add  - commit
    # book.__dict__：获取BookCreate实例的所有属性，返回一个包含属性名和值的字典
    # ** 操作符：将字典解包为关键字参数传递给Book构造函数
    # Book(...)：创建SQLAlchemy数据库模型实例
    book_obj = Book(**book.__dict__)
    db.add(book_obj)
    await db.commit()
    return book


# ----------------- 27,ORM操作数据 - 更新数据--------------------------
# 需求： 修改图书信息，先查后改
class BookUpdate(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str


@app.put("/book/update_book/{book_id}")
async def update_book(book_id: int, data: BookUpdate, db: AsyncSession = Depends(get_database)):
    # 根据book_id 先查询是否存在
    db_book = await db.get(Book, book_id)
    # 如果不存在，抛出异常
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    """
    SQLAlchemy 工作机制:
对象状态跟踪：SQLAlchemy 会监控 db_book 对象的属性变化
脏检查：当调用 commit() 时，框架会检测哪些对象被修改并生成相应的 UPDATE SQL 语句
自动同步：修改后的属性值会通过 ORM 自动同步到数据库表中
    """
    # 更新data
    db_book.bookname = data.bookname
    db_book.author = data.author
    db_book.price = data.price
    db_book.publisher = data.publisher
    # commit提交到数据库，会执行update sql语句
    await db.commit()
    return db_book


# ----------------- 28,ORM操作数据 - 删除数据--------------------------
@app.delete("/book/delete-book/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_database)):
    # 先查再删除，然后提交
    db_book = await db.get(Book, book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    await db.delete(db_book)
    await db.commit()
    return {"msg": "Book deleted successfully"}
