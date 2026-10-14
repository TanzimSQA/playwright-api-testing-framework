import pytest
from services.auth_service import AuthService
from services.product_service import ProductService
from services.cart_service import CartService
from schemas.cart_schemas import CartResponse
from config.settings import settings


@pytest.mark.e2e
@pytest.mark.regression
class TestEndToEndWorkflows:
    """End-to-End multi-step user scenarios simulating full business workflows."""

    def test_complete_e2e_shopping_journey(
        self,
        auth_service: AuthService,
        product_service: ProductService,
        cart_service: CartService,
    ):
        """
        E2E Business Workflow:
        1. Login user and retrieve JWT session token
        2. Query /auth/me with Bearer token to confirm user session
        3. Search for a product (e.g. 'laptop')
        4. Select first product and add it to cart
        5. Verify cart calculation, total items, and schema contract
        """
        # Step 1: Login
        auth_resp = auth_service.login(settings.AUTH_USERNAME, settings.AUTH_PASSWORD)
        assert auth_resp.status == 200
        auth_data = auth_resp.json()
        token = auth_data["accessToken"]
        user_id = auth_data["id"]

        # Step 2: Verify user identity
        me_resp = auth_service.get_current_user(token=token)
        assert me_resp.status == 200
        assert me_resp.json()["id"] == user_id

        # Step 3: Search for products
        search_resp = product_service.search_products(query="laptop")
        assert search_resp.status == 200
        products = search_resp.json().get("products", [])
        assert len(products) > 0
        selected_product = products[0]
        product_id = selected_product["id"]
        product_title = selected_product["title"]

        # Step 4: Add product to cart
        cart_items = [{"id": product_id, "quantity": 2}]
        cart_resp = cart_service.add_cart(user_id=user_id, products=cart_items)
        assert cart_resp.status in [200, 201]

        # Step 5: Validate cart calculations and contract
        cart_data = CartResponse.model_validate(cart_resp.json())
        assert cart_data.userId == user_id
        assert cart_data.totalQuantity >= 2
        assert len(cart_data.products) >= 1
        assert cart_data.total > 0
        assert cart_data.discountedTotal > 0
        assert cart_data.discountedTotal <= cart_data.total

        # Verify added item details
        added_product = cart_data.products[0]
        assert added_product.id == product_id
        assert added_product.quantity == 2
