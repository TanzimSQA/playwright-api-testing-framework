import pytest
from services.product_service import ProductService
from schemas.product_schemas import (
    ProductListResponse,
    ProductItem,
    ProductCreateResponse,
    ProductDeleteResponse,
)
from utils.data_generator import generate_fake_product


@pytest.mark.products
@pytest.mark.regression
class TestProducts:
    """Test suite for Product catalog, pagination, CRUD, search, and category filtering."""

    @pytest.mark.smoke
    def test_get_all_products_pagination(self, product_service: ProductService):
        """Verify fetching products list with pagination params limit and skip."""
        limit = 10
        skip = 5
        response = product_service.get_products(limit=limit, skip=skip)

        assert response.status == 200
        assert response.ok is True
        
        # Pydantic schema validation
        data = response.json()
        validated = ProductListResponse.model_validate(data)
        assert len(validated.products) == limit
        assert validated.limit == limit
        assert validated.skip == skip
        assert validated.total > 0

    @pytest.mark.smoke
    def test_get_product_by_valid_id(self, product_service: ProductService):
        """Verify fetching a single product by its unique ID."""
        product_id = 1
        response = product_service.get_product_by_id(product_id)

        assert response.status == 200
        data = response.json()
        product = ProductItem.model_validate(data)
        assert product.id == product_id
        assert product.title is not None
        assert product.price > 0

    def test_get_product_by_non_existent_id(self, product_service: ProductService):
        """Verify requesting non-existent product returns 404 Not Found."""
        non_existent_id = 999999
        response = product_service.get_product_by_id(non_existent_id)

        assert response.status == 404
        assert response.ok is False
        assert "not found" in response.text().lower()

    def test_search_products(self, product_service: ProductService):
        """Verify searching products by text query returns relevant items."""
        query = "phone"
        response = product_service.search_products(query=query)

        assert response.status == 200
        data = response.json()
        validated = ProductListResponse.model_validate(data)
        assert len(validated.products) > 0
        # Ensure at least one product has the query in title or description or category
        has_match = any(
            query in p.title.lower() or (p.description and query in p.description.lower()) or (p.category and query in p.category.lower())
            for p in validated.products
        )
        assert has_match is True, f"Search results did not contain '{query}' in title or description"

    def test_get_categories_list(self, product_service: ProductService):
        """Verify fetching category list returns non-empty collection."""
        response = product_service.get_categories()

        assert response.status == 200
        categories = response.json()
        assert isinstance(categories, list)
        assert len(categories) > 0

    def test_filter_products_by_category(self, product_service: ProductService):
        """Verify filtering products by category returns only items in that category."""
        target_category = "smartphones"
        response = product_service.get_products_by_category(target_category)

        assert response.status == 200
        data = response.json()
        validated = ProductListResponse.model_validate(data)
        assert len(validated.products) > 0
        for p in validated.products:
            assert p.category == target_category

    @pytest.mark.smoke
    def test_create_new_product(self, product_service: ProductService):
        """Verify creating a new product via POST /products/add."""
        payload = generate_fake_product()
        response = product_service.add_product(payload)

        # DummyJSON returns 201 Created (or 200) for resource creation
        assert response.status in [200, 201]
        data = response.json()
        created = ProductCreateResponse.model_validate(data)
        assert created.id > 0
        assert created.title == payload["title"]
        assert created.price == payload["price"]

    def test_update_product_put(self, product_service: ProductService):
        """Verify full update of an existing product using PUT."""
        product_id = 1
        updated_title = "Playwright Automated Test Title"
        response = product_service.update_product(product_id, {"title": updated_title})

        assert response.status == 200
        data = response.json()
        assert data.get("id") == product_id
        assert data.get("title") == updated_title

    def test_partial_update_product_patch(self, product_service: ProductService):
        """Verify partial update of an existing product using PATCH."""
        product_id = 2
        new_price = 129.99
        response = product_service.partial_update_product(product_id, {"price": new_price})

        assert response.status == 200
        data = response.json()
        assert data.get("id") == product_id
        assert data.get("price") == new_price

    def test_delete_product(self, product_service: ProductService):
        """Verify deleting a product returns deletion confirmation flag."""
        product_id = 3
        response = product_service.delete_product(product_id)

        assert response.status == 200
        data = response.json()
        deleted = ProductDeleteResponse.model_validate(data)
        assert deleted.id == product_id
        assert deleted.isDeleted is True

    @pytest.mark.parametrize("limit", [1, 5, 20])
    def test_parametrized_product_limit(self, product_service: ProductService, limit: int):
        """Parametrized test verifying various page size limits."""
        response = product_service.get_products(limit=limit)
        assert response.status == 200
        data = response.json()
        assert len(data.get("products", [])) == limit
