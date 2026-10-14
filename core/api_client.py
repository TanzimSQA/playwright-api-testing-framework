import json
import time
from typing import Any, Dict, Optional, Union
from playwright.sync_api import APIRequestContext, APIResponse as PlaywrightRawResponse
from core.logger import logger


class ApiResponse:
    """Standardized response wrapper around Playwright APIResponse."""

    def __init__(self, raw: PlaywrightRawResponse, duration_ms: float):
        self.raw = raw
        self.status: int = raw.status
        self.status_text: str = raw.status_text
        self.ok: bool = raw.ok
        self.headers: Dict[str, str] = raw.headers
        self.url: str = raw.url
        self.duration_ms: float = duration_ms
        self._cached_json: Optional[Any] = None
        self._cached_text: Optional[str] = None

    def text(self) -> str:
        if self._cached_text is None:
            try:
                self._cached_text = self.raw.text()
            except Exception:
                self._cached_text = ""
        return self._cached_text

    def json(self) -> Any:
        if self._cached_json is None:
            try:
                self._cached_json = self.raw.json()
            except Exception:
                try:
                    self._cached_json = json.loads(self.text())
                except Exception:
                    self._cached_json = None
        return self._cached_json

    def __repr__(self) -> str:
        return f"<ApiResponse [{self.status}] {self.url} ({self.duration_ms:.1f}ms)>"


class ApiClient:
    """Production-grade HTTP client wrapping Playwright sync APIRequestContext."""

    def __init__(self, request_context: APIRequestContext, base_headers: Optional[Dict[str, str]] = None):
        self.context = request_context
        self.default_headers = base_headers or {}

    def set_header(self, key: str, value: str) -> None:
        self.default_headers[key] = value

    def set_bearer_token(self, token: str) -> None:
        self.default_headers["Authorization"] = f"Bearer {token}"

    def remove_header(self, key: str) -> None:
        self.default_headers.pop(key, None)

    def _merge_headers(self, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = dict(self.default_headers)
        if custom_headers:
            headers.update(custom_headers)
        return headers

    def _send_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ApiResponse:
        merged_headers = self._merge_headers(headers)
        
        # Prepare data / json payload
        req_kwargs: Dict[str, Any] = {"headers": merged_headers}
        if params:
            req_kwargs["params"] = {k: str(v) for k, v in params.items() if v is not None}
        if data is not None:
            if isinstance(data, dict):
                req_kwargs["data"] = json.dumps(data)
                merged_headers["Content-Type"] = "application/json"
            else:
                req_kwargs["data"] = data
        if timeout:
            req_kwargs["timeout"] = timeout

        logger.info(f"==> {method.upper()} {endpoint} | Params: {params} | Headers: {list(merged_headers.keys())}")
        
        start_time = time.perf_counter()
        try:
            raw_response: PlaywrightRawResponse = getattr(self.context, method.lower())(
                endpoint, **req_kwargs
            )
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            api_response = ApiResponse(raw_response, duration_ms)
            logger.info(f"<== [{api_response.status}] {method.upper()} {endpoint} ({api_response.duration_ms:.1f}ms)")
            return api_response
        except Exception as exc:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            logger.error(f"<XX FAILED: {method.upper()} {endpoint} after {duration_ms:.1f}ms - Error: {exc}")
            raise

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ApiResponse:
        return self._send_request("get", endpoint, params=params, headers=headers, timeout=timeout)

    def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ApiResponse:
        return self._send_request("post", endpoint, params=params, data=data, headers=headers, timeout=timeout)

    def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ApiResponse:
        return self._send_request("put", endpoint, params=params, data=data, headers=headers, timeout=timeout)

    def patch(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ApiResponse:
        return self._send_request("patch", endpoint, params=params, data=data, headers=headers, timeout=timeout)

    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> ApiResponse:
        return self._send_request("delete", endpoint, params=params, headers=headers, timeout=timeout)
