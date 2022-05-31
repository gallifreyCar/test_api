import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home(data):
    return {"message": "接受到信息"}, data
uvicorn.run(app=app)
