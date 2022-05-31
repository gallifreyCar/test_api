from fastapi import FastAPI

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


@app.get('/api/hello')
async def hello():
    return {'message': 'Hello world!!'}


@app.get("/api/test")
async def home(name: str, id: int):
    return {"message": "接受到信息", "name": name, "id": id}


@app.post("/api/test2")
async def home(item: ItemModel):  # POST参数是对象
    return {"message": "接受到信息", "name": item.name, "id": item.id}


data1 = {'id': 1, 'image': 'https://npm.elemecdn.com/gallifrey-assets@1.0.4/locallive/local1.png'}
data2 = {'id': 2, 'image': 'https://npm.elemecdn.com/gallifrey-assets@1.0.4/locallive/local2.png'}
imgdata = [data1, data2]



@app.get("/api/slides")
async def home():
    return {"data": imgdata}
