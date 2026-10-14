import pytest
from services.product_service import ProductService
from services.auth_service import AuthService
from config.settings import settings


@pytest.mark.performance
class TestApiPerformanceSla:
    """Performance SLA validation tests ensuring endpoint latency thresholds are met."""

    def test_products_endpoint_latency_sla(self, product_service: ProductService):
        """Verify GET /products responds within SLA threshold."""
        response = product_service.get_products(limit=10)

        assert response.status == 200
        assert (
            response.duration_ms <= settings.MAX_RESPONSE_TIME_MS
        ), f"GET /products took {response.duration_ms:.1f}ms, exceeding SLA limit of {settings.MAX_RESPONSE_TIME_MS}ms"

    def test_single_product_endpoint_latency_sla(self, product_service: ProductService):
        """Verify GET /products/1 responds within SLA threshold."""
        response = product_service.get_product_by_id(1)

        assert response.status == 200
        assert (
            response.duration_ms <= settings.MAX_RESPONSE_TIME_MS
        ), f"GET /products/1 took {response.duration_ms:.1f}ms, exceeding SLA limit of {settings.MAX_RESPONSE_TIME_MS}ms"

    def test_auth_login_latency_sla(self, auth_service: AuthService):
        """Verify POST /auth/login responds within SLA threshold."""
        response = auth_service.login(settings.AUTH_USERNAME, settings.AUTH_PASSWORD)

        assert response.status == 200
        assert (
            response.duration_ms <= settings.MAX_RESPONSE_TIME_MS
        ), f"POST /auth/login took {response.duration_ms:.1f}ms, exceeding SLA limit of {settings.MAX_RESPONSE_TIME_MS}ms"
