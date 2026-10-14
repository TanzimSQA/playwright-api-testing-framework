from typing import Optional, Dict, Any, List, Union
from core.api_client import ApiClient, ApiResponse


class CartService:
    """Service layer for Cart endpoints."""

    def __init__(self, client: ApiClient):
        self.client = client

    def get_carts(self, limit: Optional[int] = None) -> ApiResponse:
        params = {"limit": limit} if limit else {}
        return self.client.get("/carts", params=params)

    def get_user_carts(self, user_id: Union[int, str]) -> ApiResponse:
        return self.client.get(f"/carts/user/{user_id}")

    def add_cart(self, user_id: int, products: List[Dict[str, int]]) -> ApiResponse:
        payload = {
            "userId": user_id,
            "products": products,
        }
        return self.client.post("/carts/add", data=payload)
