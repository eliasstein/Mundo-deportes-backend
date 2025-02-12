from pydantic import BaseModel

class registerproduct(BaseModel):
    name:str
    description:str
    price:float
    quantity:int
    discountPercentage:float | None = None
