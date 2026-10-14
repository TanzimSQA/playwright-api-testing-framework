import pytest
from services.user_service import UserService
from schemas.user_schemas import UserListResponse, UserItem


@pytest.mark.users
@pytest.mark.regression
class TestUsers:
    """Test suite for User endpoints and directory filtering."""

    @pytest.mark.smoke
    def test_get_users_list(self, user_service: UserService):
        """Verify fetching list of users with schema validation."""
        response = user_service.get_users(limit=5, skip=0)

        assert response.status == 200
        data = response.json()
        validated = UserListResponse.model_validate(data)
        assert len(validated.users) == 5
        assert validated.total > 0

    def test_get_user_by_id(self, user_service: UserService):
        """Verify fetching specific user by ID."""
        user_id = 1
        response = user_service.get_user_by_id(user_id)

        assert response.status == 200
        user = UserItem.model_validate(response.json())
        assert user.id == user_id
        assert user.email is not None

    def test_get_user_by_invalid_id(self, user_service: UserService):
        """Verify requesting non-existent user returns 404."""
        response = user_service.get_user_by_id(999999)

        assert response.status == 404
        assert "not found" in response.text().lower()

    def test_filter_users_by_gender(self, user_service: UserService):
        """Verify filtering users by gender attribute."""
        response = user_service.filter_users(key="gender", value="female")

        assert response.status == 200
        validated = UserListResponse.model_validate(response.json())
        assert len(validated.users) > 0
        for user in validated.users:
            assert user.gender == "female"
