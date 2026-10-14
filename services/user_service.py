from typing import Optional, Dict, Any, Union
from core.api_client import ApiClient, ApiResponse


class UserService:
    """Service layer for User directory endpoints."""

    def __init__(self, client: ApiClient):
        self.client = client

    def get_users(self, limit: Optional[int] = None, skip: Optional[int] = None) -> ApiResponse:
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if skip is not None:
            params["skip"] = skip
        return self.client.get("/users", params=params)

    def get_user_by_id(self, user_id: Union[int, str]) -> ApiResponse:
        return self.client.get(f"/users/{user_id}")

    def filter_users(self, key: str, value: str) -> ApiResponse:
        params = {"key": key, "value": value}
        return self.client.get("/users/filter", params=params)
