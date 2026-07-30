from sqlalchemy import Boolean, Column, Float, Integer, String

from backend_app.models.base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default=None)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    owner_id = Column(Integer, nullable=False)
