from typing import Optional, Dict, Any, Union
from core.api_client import ApiClient, ApiResponse


class ProductService:
    """Service layer for Products API endpoints (CRUD, search, filtering)."""

    def __init__(self, client: ApiClient):
        self.client = client

    def get_products(
        self,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        select: Optional[str] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = None,
    ) -> ApiResponse:
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if skip is not None:
            params["skip"] = skip
        if select:
            params["select"] = select
        if sort_by:
            params["sortBy"] = sort_by
        if order:
            params["order"] = order
        return self.client.get("/products", params=params)

    def get_product_by_id(self, product_id: Union[int, str]) -> ApiResponse:
        return self.client.get(f"/products/{product_id}")

    def search_products(self, query: str, limit: Optional[int] = None) -> ApiResponse:
        params: Dict[str, Any] = {"q": query}
        if limit is not None:
            params["limit"] = limit
        return self.client.get("/products/search", params=params)

    def get_categories(self) -> ApiResponse:
        return self.client.get("/products/categories")

    def get_category_list(self) -> ApiResponse:
        return self.client.get("/products/category-list")

    def get_products_by_category(self, category: str) -> ApiResponse:
        return self.client.get(f"/products/category/{category}")

    def add_product(self, product_data: Dict[str, Any]) -> ApiResponse:
        return self.client.post("/products/add", data=product_data)

    def update_product(self, product_id: Union[int, str], product_data: Dict[str, Any]) -> ApiResponse:
        return self.client.put(f"/products/{product_id}", data=product_data)

    def partial_update_product(self, product_id: Union[int, str], product_data: Dict[str, Any]) -> ApiResponse:
        return self.client.patch(f"/products/{product_id}", data=product_data)

    def delete_product(self, product_id: Union[int, str]) -> ApiResponse:
        return self.client.delete(f"/products/{product_id}")
