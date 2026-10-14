import pytest
from typing import Generator
from playwright.sync_api import sync_playwright, Playwright, APIRequestContext
from config.settings import settings
from core.api_client import ApiClient
from services.auth_service import AuthService
from services.product_service import ProductService
from services.user_service import UserService
from services.cart_service import CartService
from utils.data_generator import generate_fake_product


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Initialize Playwright instance for test session."""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="function")
def api_request_context(playwright_instance: Playwright) -> Generator[APIRequestContext, None, None]:
    """Create isolated Playwright APIRequestContext per test to prevent cookie/session leakage."""
    context = playwright_instance.request.new_context(
        base_url=settings.BASE_URL,
        extra_http_headers=settings.DEFAULT_HEADERS,
        timeout=settings.API_TIMEOUT,
    )
    yield context
    context.dispose()


@pytest.fixture(scope="function")
def api_client(api_request_context: APIRequestContext) -> ApiClient:
    """Return a fresh ApiClient instance wrapping the Playwright request context."""
    return ApiClient(api_request_context, base_headers=dict(settings.DEFAULT_HEADERS))


@pytest.fixture(scope="function")
def auth_service(api_client: ApiClient) -> AuthService:
    """Auth service fixture."""
    return AuthService(api_client)


@pytest.fixture(scope="function")
def product_service(api_client: ApiClient) -> ProductService:
    """Product service fixture."""
    return ProductService(api_client)


@pytest.fixture(scope="function")
def user_service(api_client: ApiClient) -> UserService:
    """User service fixture."""
    return UserService(api_client)


@pytest.fixture(scope="function")
def cart_service(api_client: ApiClient) -> CartService:
    """Cart service fixture."""
    return CartService(api_client)


@pytest.fixture(scope="session")
def session_auth_token(playwright_instance: Playwright) -> str:
    """Authenticate once per test session and provide access token."""
    context = playwright_instance.request.new_context(
        base_url=settings.BASE_URL,
        extra_http_headers=settings.DEFAULT_HEADERS,
    )
    client = ApiClient(context)
    service = AuthService(client)
    response = service.login(settings.AUTH_USERNAME, settings.AUTH_PASSWORD)
    
    assert response.status == 200, f"Session authentication failed: {response.text()}"
    data = response.json()
    token = data.get("accessToken") if data else None
    context.dispose()
    
    assert token, "Access token missing from login response"
    return token


@pytest.fixture(scope="function")
def authenticated_client(api_request_context: APIRequestContext, session_auth_token: str) -> ApiClient:
    """ApiClient with pre-configured Bearer token in headers."""
    client = ApiClient(api_request_context, base_headers=dict(settings.DEFAULT_HEADERS))
    client.set_bearer_token(session_auth_token)
    return client


@pytest.fixture(scope="function")
def created_product(product_service: ProductService) -> Generator[dict, None, None]:
    """Fixture that generates and creates a test product, yielding its data."""
    payload = generate_fake_product()
    response = product_service.add_product(payload)
    assert response.status == 201, f"Failed to setup created_product fixture: {response.text()}"
    product_data = response.json()
    yield product_data
    # Clean up attempt
    product_id = product_data.get("id")
    if product_id:
        product_service.delete_product(product_id)
