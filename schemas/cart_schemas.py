from typing import List, Optional
from pydantic import BaseModel


class CartProduct(BaseModel):
    id: int
    title: Optional[str] = None
    price: Optional[float] = None
    quantity: int
    total: Optional[float] = None
    discountPercentage: Optional[float] = None
    discountedTotal: Optional[float] = None
    thumbnail: Optional[str] = None


class CartResponse(BaseModel):
    id: int
    products: List[CartProduct]
    total: float
    discountedTotal: float
    userId: int
    totalProducts: int
    totalQuantity: int
