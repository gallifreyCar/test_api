from pydantic import BaseModel
class ItemModel(BaseModel):
    name:str
    id:int