from fastapi import FastAPI

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

class BaseModel():
    name:str
    id:int

@app.get("/api/test")
async def home(data :BaseModel):
    return {"message": "接受到信息"}, data
