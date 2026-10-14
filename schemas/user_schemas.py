from typing import List, Optional, Any, Dict
from pydantic import BaseModel


class UserItem(BaseModel):
    id: int
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    maidenName: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    birthDate: Optional[str] = None
    image: Optional[str] = None
    role: Optional[str] = None


class UserListResponse(BaseModel):
    users: List[UserItem]
    total: int
    skip: int
    limit: int
