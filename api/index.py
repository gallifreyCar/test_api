from fastapi import FastAPI
import pymysql
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel


class ItemModel(BaseModel):
    name: str
    id: int


app = FastAPI(
    title="Vercel FastAPI template",
    description="A starter template for FastAPI backends in Vercel deployments",
    version="0.1.0",
    docs_url='/api',
    openapi_url='/api/openapi.json',
    redoc_url=None
)


# def dbinsert(getelec,getspeed):
#     # 打开数据库连接
#     db = pymysql.connect(host='192.168.1.9',
#                          user='root',
#                          password='root',
#                          database='ssm')
#     #
#     # 使用cursor()方法获取操作游标
#     cursor = db.cursor()
#     #
#     # SQL 插入语句
#     sql = "INSERT INTO car(elec, speed) \
#                 VALUES ('%s', '%s')" % \
#           (getelec, getspeed)
#     try:
#         # 执行sql语句
#         cursor.execute(sql)
#         # 执行sql语句
#         db.commit()
#     except:
#         # 发生错误时回滚
#         db.rollback()
#
#     # 关闭数据库连接
#     db.close()


@app.get('/api/hello')
async def hello():
    return {'message': 'Hello world!!'}


@app.get("/api/test")
async def home(name: str, id: int):
    return {"message": "接受到信息", "name": name, "id": id}


@app.post("/api/test2")
async def home(item: ItemModel):  # POST参数是对象
    return {"message": "接受到信息", "name": item.name, "id": item.id}


imgdata = [{'id': 1, 'image': 'https://npm.elemecdn.com/gallifrey-assets@1.0.4/locallive/local1.png'},
           {'id': 2, 'image': 'https://npm.elemecdn.com/gallifrey-assets@1.0.4/locallive/local2.png'}]


@app.get("/api/slides")
async def home():
    return imgdata


category = [{'id': 1, 'name': '美食', 'url': 'https://npm.elemecdn.com/gallifrey-assets@1.0.5/locallive/food.png'},
            {'id': 2, 'name': '洗浴足疗', 'url': 'https://npm.elemecdn.com/gallifrey-assets@1.0.5/locallive/wash.png'},
            {'id': 3, 'name': '结婚', 'url': 'https://npm.elemecdn.com/gallifrey-assets@1.0.5/locallive/marry.png'},
            {'id': 4, 'name': '卡拉OK', 'url': 'https://npm.elemecdn.com/gallifrey-assets@1.0.5/locallive/sing.png'},
            {'id': 5, 'name': '找工作', 'url': 'https://npm.elemecdn.com/gallifrey-assets@1.0.5/locallive/work.png'},
            {'id': 6, 'name': '辅导班', 'url': 'https://npm.elemecdn.com/gallifrey-assets@1.0.5/locallive/study.png'},
            {'id': 7, 'name': '汽车保养', 'url': 'https://npm.elemecdn.com/gallifrey-assets@1.0.5/locallive/car.png'},
            {'id': 8, 'name': '租房', 'url': 'https://npm.elemecdn.com/gallifrey-assets@1.0.5/locallive/house.png'},
            {'id': 9, 'name': '装修', 'url': 'https://npm.elemecdn.com/gallifrey-assets@1.0.5/locallive/replay.png'}
            ]


@app.get("/api/categories")
async def home():
    return category


@app.get("/api/color")
async def getColor():
    colorAll = []
    for colornum in range(0, 10):
        r = random.randrange(0, 255)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)
        color = str(str(r) + ',' + str(g) + ',' + str(b))

        colorAll.append(color)
        # colorAll.append({str(r), str(g), str(b)})
        print(colorAll)

    return {"data": colorAll}


## 连接数据库

# 连接mysql数据库需要导入pymysql模块


pymysql.install_as_MySQLdb()

# 配置数据库地址：数据库类型+数据库驱动名称://用户名:密码@机器地址:端口号/数据库名
engine = create_engine("mysql+pymysql://root:root@192.168.1.9:3306/ssm", encoding='utf-8')
# 把当前的引擎绑定给这个会话；
# autocommit：是否自动提交 autoflush：是否自动刷新并加载数据库 bind：绑定数据库引擎
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 实例化
session = Session()

# declarative_base类维持了一个从类到表的关系，通常一个应用使用一个Base实例，所有实体类都应该继承此类对象
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, String, Integer


# 创建数据库模型（定义表结构:表名称，字段名称以及字段类型）
class User(Base):
    # 定义表名
    __tablename__ = 'carInfo'
    # 定义字段
    # primary_key=True 设置为主键
    id = Column(Integer, primary_key=True)
    speed = Column(String(255))
    elec = Column(String(255))

    # 构造函数
    def __init__(self, id, speed, elec):
        self.id = id
        self.speed = speed
        self.elec = elec

    # 打印形式
    def __str__(self):
        return "id:%s, speed:%s, elec:%s" % (str(self.id), self.speed, self.elec)


# 在数据库中生成表
Base.metadata.create_all(bind=engine)


# 定义数据模型
class CreatUser(BaseModel):
    id: int
    speed: str
    elec: str

    def __str__(self):
        return "id：%s, speed：%s, elec: %s" % (str(self.id), self.speed, self.elec)


## 添加单个
@app.post("/api/addInfo")
async def InserUser(data: CreatUser):
    try:
        # 添加数据
        dataNew = User(id=data.id, speed=data.speed, elec=data.elec)
        session.add(dataNew)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": "0000", "message": "添加成功"}

@app.get("/api/Get/addInfo")
async def InserUser(mid,mspeed,melec):
    try:
        # 添加数据
        dataNew = User(id=mid, speed=mspeed, elec=melec)
        session.add(dataNew)
        session.commit()
        session.close()
    except ArithmeticError:
        return {"code": "0002", "message": "数据库异常"}
    return {"code": "0000", "message": "添加成功"}



@app.get("/api/test3")
async def home(getelec, getspeed):  # POST参数是对象
    # dbinsert(getelec, getspeed)
    return {"message": "接受到信息", "elec": getelec, "speed": getspeed}
