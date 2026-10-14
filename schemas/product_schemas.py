from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class Dimensions(BaseModel):
    width: Optional[float] = None
    height: Optional[float] = None
    depth: Optional[float] = None


class Review(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None
    date: Optional[str] = None
    reviewerName: Optional[str] = None
    reviewerEmail: Optional[str] = None


class ProductItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    discountPercentage: Optional[float] = None
    rating: Optional[float] = None
    stock: Optional[int] = None
    tags: Optional[List[str]] = None
    brand: Optional[str] = None
    sku: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[Dimensions] = None
    warrantyInformation: Optional[str] = None
    shippingInformation: Optional[str] = None
    availabilityStatus: Optional[str] = None
    reviews: Optional[List[Review]] = None
    returnPolicy: Optional[str] = None
    minimumOrderQuantity: Optional[int] = None
    meta: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    thumbnail: Optional[str] = None


class ProductListResponse(BaseModel):
    products: List[ProductItem]
    total: int
    skip: int
    limit: int


class ProductCreateRequest(BaseModel):
    title: str
    price: float
    description: Optional[str] = None
    category: Optional[str] = "beauty"
    stock: Optional[int] = 100


class ProductCreateResponse(BaseModel):
    id: int
    title: str
    price: float
    description: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = None


class ProductDeleteResponse(BaseModel):
    id: int
    isDeleted: bool
    deletedOn: Optional[str] = None
