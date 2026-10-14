from typing import Optional, Dict, Any
from core.api_client import ApiClient, ApiResponse


class AuthService:
    """Service layer for authentication endpoints."""

    def __init__(self, client: ApiClient):
        self.client = client

    def login(
        self,
        username: str,
        password: str,
        expires_in_mins: Optional[int] = 30,
        headers: Optional[Dict[str, str]] = None,
    ) -> ApiResponse:
        payload = {
            "username": username,
            "password": password,
            "expiresInMins": expires_in_mins,
        }
        return self.client.post("/auth/login", data=payload, headers=headers)

    def get_current_user(self, token: Optional[str] = None) -> ApiResponse:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return self.client.get("/auth/me", headers=headers)

    def refresh_token(self, refresh_token: str) -> ApiResponse:
        payload = {"refreshToken": refresh_token}
        return self.client.post("/auth/refresh", data=payload)
