from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
    description: str | None = None
    class Config:
        form_attributes=True

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    description: str | None = None

    class Config:
        form_attributes=True
