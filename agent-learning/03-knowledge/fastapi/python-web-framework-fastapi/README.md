# python_web框架-FastAPI

#### 介绍

跟着b站黑马程序员2025-12-10的课程（https://www.bilibili.com/video/BV1zV2QBtE39）学习python的web框架：FastAPI。
FastAPI框架的官方中文文档：https://fastapi.org.cn/#opinions
加油干！

#### 软件架构

软件架构说明

#### 安装教程

1. 请根据具体情况修改下面的数据库配置。
2. ```python
   # 1. 创建异步引擎
   ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/fastapi_first?charset=utf8"
   ```
3. 自行在book表添加数据

```sql
insert into book(id, bookname, author, price, publisher, create_time, update_time) values
('1', '红楼梦', '曹雪芹', '22', '黑马', '2026-01-12 22:11:00', '2026-01-12 22:11:00'),
('2', '西楼梦', '吴承恩', '45', '金乌', '2026-01-13 20:11:00', '2026-01-13 20:11:00'),
('3', '西门子', '吴晓恩', '34', '京东', '2026-01-13 20:30:00', '2026-01-13 20:30:00'),
('4', '红楼梦1', '曹雪', '16', '黑马', '2026-01-12 22:11:00', '2026-01-12 22:11:00');
```

1. xxxx

#### 使用说明

1. xxxx
2. xxxx
3. xxxx

#### 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

#### 特技

1. 使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2. /assets 文件夹存储README.md中的图片
3. 大模型工程师核心能力：

- Python基础：语言基础
- 服务化能力：通过Python Web框架将模型从本地代码部署为在线可访问、可扩展且稳定运行的服务
- AI大模型开发能力：模型训练、构建、微调、优化等

一个Web项目 + 一个AI项目：掌握独立搭建Web后端项目的能力、掌握AI模型的部署与服务化能力、
形成清晰的编程思维与工程化意识、高效运用AI工具辅助开发能力

#### 02_fastapi框架简介

1. 异步性能高
2. 下载fastapi      pip install "fastapi[standard]"
3. 类型提示与验证     Pydantic类型提示与验证，减少手动校验代码
4. 可交互式文档       自动生成可交互式文档，浏览器中直接调用和测试API    127.0.0.1:8000/docs
5. 要在main.py里面运行fastapi才行，运行命令 fastapi dev main.py

![img.png](assets/img.png)

![img_1.png](assets/img_1.png)

![img_2.png](assets/img_2.png)

#### 03_第一个FastAPI程序

1. 创建虚拟环境：.venv 隔离项目运行环境，避免依赖冲突，保持全局环境的干净和稳定
2. 启动fastapi应用命令：  uvicorn main:app --reload
3. uvicorn - ASGI 高性能服务器，用于运行 FastAPI 应用

![image-20260110184556246](assets/image-20260110184556246.png)

#### 04_路由

```python
# 路由是URL地址和处理函数之间的映射关系
```

![image-20260110194943409](assets/image-20260110194943409.png)

#### 05_参数简介和路径参数

路径参数：

- 位置：URL路径的一部分               /book/{id}
- 作用：指向唯一的、特定的资源
- 方法：GET

查询参数：

- 位置：URL？之后k1=v1&k2=v2
- 作用：对资源集合进行过滤、排序、分页等操作
- 方法：GET

请求体：

- 位置：HTTP请求的消息体{body}中
- 作用：创建、更新资源、携带大量数据，如JSON数据
- 方法：POST、PUT

#### 06_路径参数__Path类型注解

```python
from fastapi import FastAPI,Path,Query
```

```python
# 路径参数    路径参数传到处理函数的形参中   id: int 参数类型注解
@app.get("/book/{id}")                #...表示必填，gt大于，lt小于，description描述
async def get_book(id: int = Path(..., gt=0, lte=101, descripion ='书籍id，取值范围【1-101】')):
    return {
        "id": id,
        "title": f"这是第{id}本书"
    }
# 需求：查找书籍的作者，路径参数 name，长度范围2-10
@app.get("/author/{name}")
async def get_name(name: str=Path(..., min_length=2, max_length=10)):
    return {"msg": f"这是{name}作者的信息"}
```

路径参数是URL路径的一部分    /book/{book_id}

路径参数添加类型注解：Python原生注解和Path注解

#### 07_查询参数__Query类型注解

```python
from fastapi import FastAPI,Path,Query
```

![image-20260111173118676](assets/image-20260111173118676.png)

- 查询参数出现在URL？之后，k=v&k=v
- 查询参数添加类型注解：Python原生注解和Query注解

```python
# 需求 查询新闻 -> 分页，skip：跳过的记录数， limit：返回的记录数 10
@app.get("/news/list/news_list")
async def get_news_list(
        skip: int = Query(0, description="跳过的记录数", lt=100),
        limit: int = Query(10, description="返回的记录数")):  # 默认就是查询参数 URL?k=v&k=v
    return {
        "skip": skip,
        "limit": limit
    }
```

#### 08_请求体参数

```python
from pydantic import BaseModel,Field
```

![image-20260111181808950](assets/image-20260111181808950.png)

![image-20260111182041114](assets/image-20260111182041114.png)

```python
# ---------------------------请求体参数---------------------------------
class User(BaseModel):
    username: str
    password: str

# 需求：注册用户
@app.post("/user/register")
async def register(user: User):
    return user

class Book(BaseModel):
    name: str            # 书名
    author: str          # 作者
    publisher: str       # 出版社
    sell_price: float    # 销售价格

# 需求：新增图书
@app.post("/book/create")
async def create_book(book: Book):
    return book
```

#### 09_请求体参数__Field类型注解

![image-20260111183427544](assets/image-20260111183427544.png)

```python
class User(BaseModel):
    username: str = Field(default="张三", min_length=2, max_length=10, description="用户名，长度要求2-10个字符")
    password: str = Field(min_length=3, max_length=20)

# 需求：注册用户
@app.post("/user/register")
async def register(user: User):
    return user

# Field(default="") 没有default默认值。...表示必填
class Book(BaseModel):
    name: str = Field(..., min_length=2, max_length=20)            # 书名
    author: str = Field(..., min_length=2, max_length=10)          # 作者
    publisher: str = Field(default="黑马程序员")                     # 出版社
    sell_price: float = Field(...,gt=0)                            # 销售价格

# 需求：新增图书
@app.post("/book/create")
async def create_book(book: Book):
    return book
```

![image-20260111184915201](assets/image-20260111184915201.png)

#### 10_响应类型-JSON格式

默认情况下，**FastAPI会自动将路径操作函数返回的Python对象（字典、列表、Pydantic模型等），经由jsonable_encoder转换为JSON兼容格式，并包装为JSONResponse返回**。这省去了手动序列化的步骤，让开发者能更专注于业务逻辑。

如果需要返回非JSON数据（如HTML、文件流），FastAPI提供了丰富的响应类型来返回不同数据。

![image-20260111200951097](assets/image-20260111200951097.png)

#### 11_响应类型-HTML格式：HTMLResponse

```python
from fastapi.responses import HTMLResponse
```

![image-20260111202311068](assets/image-20260111202311068.png)

装饰器中指定响应类

```py
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
```

#### 12_响应类型-文件格式：FileResponse

![image-20260111203633350](assets/image-20260111203633350.png)

```python
# 接口：返回文件
@app.get("/file")
async def get_file():
    path = "./assets/img.png"
    return FileResponse(path)
```

#### 13_自定义响应数据格式: response_model

**response_model**是路径操作装饰器（如@app.get或@app.post)的关键参数，它通过一个**Pydantic模型来严格定义和约束API端点的输出格式**。这一机制在提供自动数据验证和序列化的同时，更是保障数据安全性的第一道防线。

![image-20260111210508554](assets/image-20260111210508554.png)

```python
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
        "content": f"这是第{id}条新闻的内容"
    }
```

#### 14_异常响应处理

```python
from fastapi import FastAPI,Path,Query,HTTPException
```

![image-20260111213516520](assets/image-20260111213516520.png)

```py
# ------------------异常处理 raise HTTPException(status_code=404, detail="报错了，xxx") ----------------------------
# 需求：根据id查询新闻 -> 1-6
@app.get("/news/httpexception/{id}")
async def get_news(id: int):
    id_list = [1, 2, 3, 4, 5, 6]
    if id not in id_list:
        raise HTTPException(status_code=404, detail="你查找的新闻不存在")
    return {"id": id, "title": f"这是第{id}条新闻"}
```

#### 15_中间件middleware

使用中间件为每个请求前后添加统一的处理逻辑。例如：日志记录、身份认证、跨域处理、响应头处理、性能监控。

![image-20260112171446305](assets/image-20260112171446305.png)

![image-20260112171610713](assets/image-20260112171610713.png)

中间件Middleware是一个<u>在每次请求进入FastAPI应用时都会被执行的函数</u>。它在请求到达实际的路径操作（路由处理函数）之前运行，并且在响应返回给客户端之前再运行一次。

![image-20260112172132044](assets/image-20260112172132044.png)

语法：

```python
@app.middleware("http")
async def middleware(request, call_next):
    print("中间件开始处理  --  start")
    response = await call_next(request)
    print("中间件处理完成 -- end")
    return response
```

![image-20260112172355280](assets/image-20260112172355280.png)

```python
# async 代表异步函数。真有异步代码await要带上。
@app.middleware("http")
async def middleware(request, call_next):     # request是请求，call_next是传递请求的函数名
    print("中间件1开始处理  --  start")
    response = await call_next(request)       # 这里就有异步代码
    print("中间件1处理完成 -- end")
    return response

# async 代表异步函数。真有异步代码考艾要搭上
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
```

![image-20260112180133115](assets/image-20260112180133115.png)

#### 16_依赖注入

1. 使用**依赖注入系统**来共享通用逻辑，减少代码重复。依赖项（可重用的组件）来实现。

![image-20260112180715260](assets/image-20260112180715260.png)

![image-20260112180915055](assets/image-20260112180915055.png)

2. 依赖注入应用场景：处理请求参数、共享业务逻辑、共享数据库连接、安全和认证。

![image-20260112181213219](assets/image-20260112181213219.png)

3. 依赖注入的作用域：

FastAPI依赖注入主要有三个级别，区别在于作用域不同：

- 路径级别（Path Operation）：最常用，注入到@app.get() / @router.post() 等装饰器下面的函数中

```python
# ---------------------------------路径级依赖注入--------------------------------

# 依赖函数：检查用户权限
def check_user_permission(authorization: str = Header(...)):
    """
    检查用户权限的依赖函数
    支持 Authorization: Bearer <token> 格式
    """
    # 提取 Bearer token 中的实际 token 值
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
```

- 路由级别-共享依赖（APIRouter）：将依赖注入到整个路由器下的所有路径操作

```python
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
```

- 全局级别-全局依赖（FastAPI）：将依赖注入到整个应用的所有路径操作

```python
# ----------------------------全局级别依赖注入----------
# 依赖函数：对所有API记录请求信息
async def log_request(request: Request):
    print(f"Request received: {request.method}%s{request.url}" % " ")
    return {"logged": True}
app = FastAPI(dependencies=[Depends(log_request)])
```



共享参数依赖函数的使用方式

```python
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
```



4. 语法：先创建依赖项，然后声明依赖项。Depends(依赖项)

![image-20260112181339047](assets/image-20260112181339047.png)

```py
# 需求：分页参数逻辑共用：新闻列表和用户列表     16-1.定义依赖项（请求参数共用）
async def common_parameters(
        skip: int = Query(0, ge=0),         # skip跳过 >= 0
        limit: int = Query(10, le=60)       # page_size默认值10，范围0-60
):
    return {"skip": skip, "limit": limit}

# 查询参数 URL?k=v&k=v       ； 16-2.声明依赖项commons=Depends(common_parameters)
@app.get("/news_16/news_list")
async def get_news_list(commons=Depends(common_parameters)):
    return commons

# 查询参数 URL?k=v&k=v      ；声明依赖项commons=Depends(common_parameters)
@app.get("user_16/user_list")
async def get_user_list(commons=Depends(common_parameters)):
    return commons
```



5. 嵌套依赖注入

![image-20260127184112159](assets/image-20260127184112159.png)

```py
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
```



6. 类依赖

![image-20260127191437091](assets/image-20260127191437091.png)

![image-20260127191722070](assets/image-20260127191722070.png)



#### 17_ORM简介和安装

![image-20260112190131282](assets/image-20260112190131282.png)

学ORM框架：SQLAlchemy

![image-20260112190213516](assets/image-20260112190213516.png)

![image-20260112190252313](assets/image-20260112190252313.png)

#### 18_ORM建表

![image-20260112202617447](assets/image-20260112202617447.png)

![image-20260112203257105](assets/image-20260112203257105.png)

```python
# ------------------------- 18_ORM安装和建表 -----------------------
# pip install sqlalchemy
# pip install aiomysql

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func, DateTime, String, Float, select

# 1. 创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/fastapi_first?charset=utf8"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,            # 可选，输出SQL日志
    pool_size=10,         # 设置连接池活跃的连接数
    max_overflow=20,      # 允许额外的连接数
)

# 2. 定义模型类： 基类 + 表对应的模型类
# 基类：创建时间、更新时间；书籍表：id、书名、作者、价格、出版社
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now,comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime,insert_default=func.now, default=func.now, onupdate=func.now, comment="更新时间",)

class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str] = mapped_column(String(255),comment="出版社")

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, comment="用户id")
    username: Mapped[str] = mapped_column(String(255), comment="用户名")
    password: Mapped[str] = mapped_column(String(255), comment="密码")

# 3. 建表：定义函数建表   FastAPI启动时候调用建表的函数
async def create_tables():
    # 获取异步引擎，创建事务  - 建表             as 别名。。。async with  异步上下文管理器。
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)          # 继承了Base模型类的元数据（表），都会被创建

# app启动时候，创建表
@app.on_event("startup")
async def startup_event():
    await create_tables()
```

#### 19_ORM__在路由中使用ORM

核心：创建依赖项，使用Depends注入到路由处理函数。

创建获取数据库会话依赖项，

![image-20260112215310328](assets/image-20260112215310328.png)

```python
#-------------------------- 19_在路由中使用ORM -----------------------
# 需求：查询功能的接口，查询图书 。依赖注入：创建依赖项获取数据库会话 + Depends 注入路由处理函数
AsyncSessionLocal =  async_sessionmaker(
    bind=async_engine,            # 绑定数据库引擎
    class_=AsyncSession,          # 指定会话类
    expire_on_commit=False        # 提交后会话不过期，不会重新查询数据库
)

# 依赖项：获取数据库会话
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session          # 返回数据库会话给路由处理函数
            await session.commit()  # 提交事务
        except Exception:
            await session.rollback()   # 有异常，回滚
            raise
        finally:
            await session.close()       # 关闭会话

@app.get("/book/books")
async def get_book_list(db: AsyncSession = Depends(get_database)):
    # 看下依赖有没有注入成功。
    # 查询
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books
```

上述代码与18是一块的。

#### 20_ORM操作数据-查询数据

```py
await db.execute(select(模型类))`
```

![image-20260113200758573](assets/image-20260113200758573.png)

```python
# -----------------------20_ORM查询数据------------------------------
@app.get("/book/books")
async def get_book_list(db: AsyncSession = Depends(get_database)):
    # # 查询书籍列表     看下依赖有没有注入成功。注入数据库会话
    # result = await db.execute(select(Book))     # 查询 返回一个ORM对象
    # books = result.scalars().all()      # 获取所有书籍
    # book = result.scalars().first()     # 获取第一条数据
    book = await db.get(Book, 2)    # 根据id主键获取单条数据
    return book
```

```python
# 需求：路径参数：数据ID
@app.get("/book/book_detail/{book_id}")
async def get_book_detail(book_id: int, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book_detail = result.scalar_one_or_none()
    return book_detail

# 需求：条件查询 价格大于等于30
@app.get("/book/search_book")
async def get_search_book(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.price >= 30))
    books = result.scalars().all()
    return books
```

#### 21_ORM操作数据--条件查询--比较判断

```py
select(Book).where(条件,条件2,....)
```

![image-20260113202252668](assets/image-20260113202252668.png)

例如：

![image-20260113202254963](assets/image-20260113202254963.png)

#### 22_ORM查询数据 条件查询-模糊查询&与非&包含

![image-20260116184425545](assets/image-20260116184425545.png)

```python
# ---------------22_ORM查询数据 条件查询-模糊查询&与非&包含----------------
# 需求 ：作者以 曹开头 %
@app.get("/book/search_book_by_author_like")
async def search_book_by_author_like(db: AsyncSession = Depends(get_database)):
    # where(Book.column.like("value%"))  1.模糊查询
    # result = await db.execute(select(Book).where(Book.author.like("曹%")))
    # result = await db.execute(select(Book).where(Book.author.like("曹_")))

    # 2. where( (条件1) & (条件2) )  与            where( (条件1) | (条件2) )  或         where( ~(条件) )  非
    # result = await db.execute(select(Book).where(~(Book.author.like("曹%")) | (Book.price >= 20)))
    # result = await db.execute(select(Book).where((Book.author.like("曹%")) & (Book.price >= 20)))

    # 3. 需求：书籍id列表，数据库里面的id如果在书籍id列表里面，就返回能查询得到的
    id_list = [1,2,4,999]
    result = await db.execute(select(Book).where(Book.id.in_(id_list)))
    books = result.scalars().all()
    return books
```

#### 23，ORM操作数据 - 聚合查询

![image-20260116184606749](assets/image-20260116184606749.png)

```python
# -------------------23,ORM查询数据，聚合查询 min,max,avg,--------------------------
@app.get("/book/count")
async def get_count(db: AsyncSession = Depends(get_database)):
    # result=  await db.execute(select(func.max(Book.price)))
    # result=  await db.execute(select(func.min(Book.price)))
    result=  await db.execute(select(func.avg(Book.price)))
    # 计算多少行
    # result =  await db.execute(select(func.count(Book.id)))
    return result.scalar()    # 用来提取一个数据 = > 标量值
```

#### 24，ORM操作数据，分页查询

```python
# --------------------21，ORM数据库操作，ORM分页炒作---------------------
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
```

#### 25，ORM查询，总结

select()  ->  db.execute()  -  从ORM对象获取数据   -   响应结果

条件查询 where()                聚合查询func.xxxx         分页查询offset()  limit()

比较                                       count()                              select().offset().limit()

模糊                                       max()  and  min()      offset = (current_page-1) * page_size

与或非                                    avg()

包含                                        sum()

对ORM对象获取数据的方式

获取所有数据   scalars().all()

获取单条数据

scalars().first()                  获取第一个数据

scalar_one_or_none()     提取一个或者NULL

scalar()                              提取标量值（配合聚合查询使用）

#### 26,ORM操作数据，添加数据

核心步骤：定义ORM对象  --   添加对象到事务：add(对象)   -> commit提交到数据库

```python
# ----------------- 26,ORM操作数据，添加数据--------------------------
# 需求：用户输入图书信息（id、书名、作者、价格、出版社）。使用HTTP请求体传递用户输入数据
class BookCreate(BaseModel):
    id: int
    bookname: str
    author: str
    price: float
    publisher: str

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
```

#### 27,ORM操作数据 - 更新数据

![image-20260116201123236](assets/image-20260116201123236.png)

```python
# ----------------- 27,ORM操作数据 - 更新数据--------------------------
# 需求： 修改图书信息，先查后改
class BookUpdate(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str

@app.put("/book/update_book/{book_id}")
async def update_book(book_id: int,data: BookUpdate, db: AsyncSession = Depends(get_database)):
    # 根据book_id 先查询是否存在
    db_book = await db.get(Book, book_id)
    # 如果不存在，抛出异常
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # 更新data
    db_book.bookname = data.bookname
    db_book.author = data.author
    db_book.price = data.price
    db_book.publisher = data.publisher
    # 提交到数据库
    await db.commit()
    return db_book
```

#### 28，ORM操作数据 - 删除数据

核心步骤：查询get  -  delete删除  ---  commit提交到数据库

![image-20260116202545646](assets/image-20260116202545646.png)

```python
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
```

#### 29，sqlalchemy进行CURD操作

![image-20260116204300045](assets/image-20260116204300045.png)

### 30，AI掘金头条新闻系统

![image-20260116214622166](assets/image-20260116214622166.png)

![image-20260116214744183](assets/image-20260116214744183.png)

![image-20260116215113284](assets/image-20260116215113284.png)

![image-20260116215133391](assets/image-20260116215133391.png)

![image-20260116215159993](assets/image-20260116215159993.png)

![image-20260116215256705](assets/image-20260116215256705.png)

![image-20260116215446645](assets/image-20260116215446645.png)

![image-20260116215600261](assets/image-20260116215600261.png)

![image-20260116215656674](assets/image-20260116215656674.png)

![image-20260116215709312](assets/image-20260116215709312.png)

![image-20260116215745540](assets/image-20260116215745540.png)

![image-20260116215857574](assets/image-20260116215857574.png)

![image-20260116220906178](assets/image-20260116220906178.png)

![image-20260117113626611](assets/image-20260117113626611.png)

#### 31，工程结构

packages：

crud  数据库增删改查逻辑（封装数据库操作）

models  数据库模型（SQLAlchemy ORM）

routers  路由层（按照模块划分）

schemas  数据验证模型（Pydantic数据校验）

utils   工具函数

config   配置相关

![image-20260117100036824](assets/image-20260117100036824.png)

#### 32 模块化路由

![image-20260117144425445](assets/image-20260117144425445.png)

![image-20260117150242312](assets/image-20260117150242312.png)

```python
from fastapi import APIRouter

# 创建APIRouter实例。prefix 路由前缀。tags 分组标签。需要app挂载一下app.include_router(news.router)
router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories():
    return {"msg": "获取分类成功"}
```

#### 33，数据库和ORM配置

![image-20260117150512986](assets/image-20260117150512986.png)

![image-20260117151009272](assets/image-20260117151009272.png)

#### 34，获取新闻分类

![image-20260117154019414](assets/image-20260117154019414.png)

```py
# 接口实现流程
# 1. 模块化路由  API接口规范文档
# 2. 定义模型类  数据库表结构（数据库设计文档）
# 3. 在curd文件夹里面创建文件，封装操作数据库的方法
# 4. 在路由处理函数里面调用curd封装号的方法，响应结果
```

#### 36，解决跨域问题

![image-20260117165940546](assets/image-20260117165940546.png)

![image-20260117170006530](assets/image-20260117170006530.png)

![image-20260117170600779](assets/image-20260117170600779.png)

```py
# 解决跨域问题
app.add_middleware(CORSMiddleware,
                    allow_origins=["*"],    #允许的源，prod环境建议指定允许的域名列表
                    allow_credentials=True, # 允许携带cookie
                    allow_methods=["*"],    # 允许的请求方法
                    allow_headers=["*"],    # 允许的请求头
                    )
```

#### 37-40

![image-20260117201300485](assets/image-20260117201300485.png)

更新字段：

```py
# 增加新闻浏览量
async def increase_news_views(db: AsyncSession, news_id: int):
    # 浏览量+1
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新后，检查数据库是否真的命中了数据，命中了返回True
    return result.rowcount > 0
```

列表推导式：  order_by排序：

```py
# 获取当前新闻的关联新闻
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    # order_by 排序。按照浏览量和发布时间进行排序
    stmt = select(News).where(News.category_id == category_id ,News.id != news_id).order_by(News.views.desc(), News.publish_time.desc()).limit(limit)
    result = await db.execute(stmt)
    # return result.scalars().all()
    related_news = result.scalars().all()
    # 列表推导式，推导出新闻的核心数据，然后再return
    return [{
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "image": news.image,
        "author": news.author,
        "publishTime": news.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
        "categoryId": news.category_id,
        "views": news.views,
    } for news in related_news]
```

![image-20260117203650099](assets/image-20260117203650099.png)

#### 41项目总结

![image-20260117203800178](assets/image-20260117203800178.png)

![image-20260117204043055](assets/image-20260117204043055.png)

---

## UV

官方文档：(https://docs.astral.sh/uv/getting-started/features/#tools)

uv管理项目依赖：第三方python依赖包和环境。一个极其快速的 Python 包和项目管理器，用 Rust 编写。

### [Projects](https://docs.astral.sh/uv/getting-started/features/#projects)

Creating and working on Python projects, i.e., with a `pyproject.toml`.

- `uv init`: Create a new Python project.
- `uv add`: Add a dependency to the project.
- `uv remove`: Remove a dependency from the project.
- `uv sync`: Sync the project's dependencies with the environment.
- `uv lock`: Create a lockfile for the project's dependencies.
- `uv run`: Run a command in the project environment.
- `uv tree`: View the dependency tree for the project.
- `uv build`: Build the project into distribution archives.
- `uv publish`: Publish the project to a package index.

### [Working on projects 进行项目工作](https://docs.astral.sh/uv/guides/projects/#working-on-projects)

uv supports managing Python projects, which define their dependencies in a `pyproject.toml` file.
uv 支持管理 Python 项目，这些项目在其 `pyproject.toml` 文件中定义了它们的依赖项。**也就是说，如果项目用UV管理python第三方依赖包，则会在pyproject.toml文件定义这个项目所需要的依赖以及版本号**

### [Project structure 项目结构](https://docs.astral.sh/uv/guides/projects/#project-structure)

A project consists of a few important parts that work together and allow uv to manage your project. In addition to the files created by `uv init`, uv will create a virtual environment and `uv.lock` file in the root of your project the first time you run a project command, i.e., `uv run`, `uv sync`, or `uv lock`.
一个项目由几个重要部分组成，这些部分协同工作，允许 uv 管理你的项目。除了 `uv init` 创建的文件外，当你第一次运行项目命令（即 `uv run` 、 `uv sync` 或 `uv lock` ）时，uv 还会在你的项目根目录中创建一个虚拟环境和 `uv.lock` 文件。

A complete listing would look like:
完整的列表如下：

.
├── .venv
│   ├── bin
│   ├── lib
│   └── pyvenv.cfg
├── .python-version
├── README.md
├── main.py
├── pyproject.toml
└── uv.lock

就是uv.lock、pyproject.toml、.python-version都是UV的东西

----------------------------------------------------------------------------------------------------

```python
# 设计模式：装饰器模式
# api 版本路由

v1_router = APIRouter(prefix="/api/v1")

# 模块路由

user_router = APIRouter(tags=["用户"], prefix="/user")
item_router = APIRouter(tags=["物品"], prefix="/item")

# app包含版本，版本包含模块

v1_router.include_router(user_router)
v1_router.include_router(item_router)
app.include_router(v1_router)
```



#### 项目结构

将代码拆分为多个文件和目录是更有的实践，主要原因：

1. 职责分离：每个文件或目录是系统的一个组成部分（数据库配置、模型、模式、路由、中间件等）,使代码结构清晰
2. 提高代码可读性和可维护性
3. 增加可扩展性：业务进行扩展时，只需添加新的文件或目录，而不需要修改现有的文件或目录。
4. 清晰的依赖管理：通过显示导入依赖
5. 便于团队协作
6. 符合企业级项目规范



#### 项目结构示例

按照软件功能目录结构

![image-20260123195338887](assets/image-20260123195338887.png)

 基于DDD领域驱动设计，就是按照业务模块进行划分

![image-20260123195438225](assets/image-20260123195438225.png)



## DDD（Domain-Driven Design） 领域驱动设计 

https://www.bilibili.com/video/BV1eKpizeEnb

#### 55，了解DDD领域驱动设计的核心概念

1. DDD的核心思想

- **业务优先**：先搞懂业务是怎么运作的，而不是一上来就建表
- **统一语言**：程序员、产品经理、业务方用同一个词描述同一个东西
- **边界清晰**：把大系统拆分成几个“小王国”，每个王国自己管自己

2. DDD核心概念

- **领域：**软件要解决的哪个业务范围
- **通用语言：**团队里所有人（程序员、产品经理、测试等）约定好的一套“黑话”。讨论业务、写代码、写文档都用这套话，不准出现第二种说法。DDD的基石。
- **限界上下文：给“通用语言”划界限**。同一个词，在不同的部门（上下文）里，意思可能完全不同。界限上下文就是把这些部门隔开，让每个部门内部用自己的“方言”而不会混乱。

![image-20260127204908547](assets/image-20260127204908547.png)

关键点：你不能把这三个上下文的"订单"混在一起设计成一个巨无霸Order类，会复杂到爆炸。限界上下文就是告诉你，应该把它们当成三个不同的东西来开发，甚至可以做成三个不同的微服务。这是降低复杂度的超级大招。

- **实体：有唯一ID的东西**，你看重的是“他是谁”，而不是它“是什么样”。它会变化，但它的身份ID不变。
- **值对象: 没ID, 只看属性值的东西。**你看重的是“它是什么样”, 如果两个东西的所有属性值一样, 就可以认为是它们是同一个东西。

![image-20260127212313750](assets/image-20260127212313750.png)

- **聚合根：一组相关对象的“老大”。**外部只能通过它来访问这组对象，它是保证业务一致性的边界。

![image-20260127212513044](assets/image-20260127212513044.png)

例如A是老大，A1、A2是A的小弟。修改A1要通过A.modify_a1()方法才行。

**为什么需要聚合根？**

![image-20260127212920951](assets/image-20260127212920951.png)

- **领域服务：**处理那些不属于任何实体/值对象的业务逻辑，通常是跨聚合的、无状态的、需要协调多个领域对象的操作。

![image-20260127213242722](assets/image-20260127213242722.png)



#### 56，DDD领域驱动设计的分层架构

DDD领域驱动设计推荐的分层架构，各层职责明确、依赖单向，确保业务核心（领域层）不受技术细节污染。

![image-20260127215400114](assets/image-20260127215400114.png)

##### 一，**用户接口层（User Interface Layer）**

1. **别名：**表现层，Web层，接口层，Controller层

2. **职责：**

  ​	2.1 接收外部请求（如HTTP、RPC、CLI）

  ​	2.2 解析输入参数（如JSON、表单）

  ​	2.3 执行基础校验（如非空、格式）

  ​	2.4 调用应用层服务完成业务操作

  ​	2.5 返回响应结果（如JSON、页面）

3. **不包含：**

  3.1 业务规则判断

  3.2 领域逻辑

4. **依赖:**
    4.1 仅依赖应用层（调用应用服务）。
    4.2 示例OrderController -> PlaceOrderService



##### 二，应用层（Application Layer）

1. 别名：用例层、服务门面层

2. 职责：
   2.1 协调领域对象完成一个完整的业务用力（如下单、转账）

   2.2 处理事务边界（如开启事务）
   2.3 发布领域实践

   2.4 转换DTO（数据传输对象）

   2.5 不包含可信业务规则（只指挥，不决策）

   

3. 组件示例：

​	3.1 应用服务（PlaceOrderService）

​	3.2 Command/Query对象

​	3.3 DTO（Data Transfer Object）

4. 依赖：

​	4.1 依赖**领域层**（使用实体、聚合、领域服务)

​	4.2 依赖**基础设施层**（获取Repository实现）

​	4.3 被**用户界面层**调用



##### **三，领域层（Domain Layer）**

1. 别名：模型层、核心层

2. 职责
   2.1 包含系统的核心业务逻辑和规则

   2.2 定义领域模型：
   	实体
   	值对象
   	聚合根

   ​	领域服务

   ​	领域事件

   2.3 保证业务一致性（如订单金额不能为负）

   2.4 不依赖任何外部框架（如Djiango、FastAPI、SQLAlchemy）

3. 关键原则：

   3.1 业务逻辑必须在这里实现

   3.2 聚合根负责维护内部一致性

4. 依赖

   4.1 无依赖（理想情况下不依赖其他层）

   4.2 被**应用层**调用

四，基础设施层（Infrastructure Layer）

1. 别名：数据访问层、技术实现层

2. 职责：

   2.1 提供技术实现，支撑上层运行

   2.2 实现领域层定义的接口。例如：OrderRepositroy接口的具体实现（如JPA、MyBatis）；消息队列发送器（如KafkaProducer）；外部API调用（如支付网关）

   2.3 处理数据库、缓存、文件、邮件等底层操作

3. 组件示例：

   3.1 Repository实现类

   3.2 事件发布器

   3.3 第三方客户端

4. 依赖

   4.1 依赖**领域层**（实现其接口）

   4.2 依赖**应用层**（如监听应用事件）

   4.3 被**应用层**和**领域事件处理器**调用

![image-20260127222550985](assets/image-20260127222550985.png)



#### 57_DDD的项目基础设置

![image-20260128211312625](assets/image-20260128211312625.png)































