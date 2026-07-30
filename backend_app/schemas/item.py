from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    in_stock: bool = True


class ItemUpdate(BaseModel):
    name: str
    description: str | None = None
    price: float
    in_stock: bool = True


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    in_stock: bool
    owner_id: int

    class Config:
        from_attributes = True
