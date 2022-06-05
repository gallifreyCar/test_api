from fastapi import FastAPI
import pymysql
import random
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



def dbinsert(getelec,getspeed):
    # 打开数据库连接
    db = pymysql.connect(host='192.168.1.9',
                         user='root',
                         password='root',
                         database='ssm')
    #
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    #
    # SQL 插入语句
    sql = "INSERT INTO car(elec, speed) \
                VALUES ('%s', '%s')" % \
          (getelec, getspeed)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    db.close()


@app.get('/api/hello')
async def hello():
    return {'message': 'Hello world!!'}


@app.get("/api/test")
async def home(name: str, id: int):
    return {"message": "接受到信息", "name": name, "id": id}


@app.post("/api/test2")
async def home(item: ItemModel):  # POST参数是对象
    return {"message": "接受到信息", "name": item.name, "id": item.id}


@app.get("/api/test3")
async def home(getelec, getspeed):  # POST参数是对象
    dbinsert(getelec, getspeed)
    return {"message": "接受到信息", "elec": getelec, "speed": getspeed}



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


