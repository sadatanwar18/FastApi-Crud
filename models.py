from pydantic import BaseModel

class productBase(BaseModel):
 
    name : str
    description: str
    price: float
    quantity: int

class ProductCreate(productBase):
    pass

class Product(productBase):
    id:int

    class Config:
        orm_mode = True