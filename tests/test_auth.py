import pytest
from config.settings import settings
from services.auth_service import AuthService
from schemas.auth_schemas import LoginSuccessResponse, AuthErrorResponse, CurrentUserResponse
from utils.data_generator import generate_fake_credentials


@pytest.mark.auth
@pytest.mark.smoke
class TestAuthentication:
    """Test suite for authentication, tokens, and authorization security."""

    def test_login_successful_with_valid_credentials(self, auth_service: AuthService):
        """Verify successful login returns 200 OK, valid JWT accessToken, and matches schema."""
        response = auth_service.login(
            username=settings.AUTH_USERNAME,
            password=settings.AUTH_PASSWORD,
            expires_in_mins=60,
        )

        assert response.status == 200, f"Expected 200 OK, got {response.status}"
        assert response.ok is True
        assert "application/json" in response.headers.get("content-type", "")

        # Pydantic schema validation
        data = response.json()
        validated_data = LoginSuccessResponse.model_validate(data)
        assert validated_data.username == settings.AUTH_USERNAME
        assert len(validated_data.accessToken) > 20
        assert validated_data.id == 1

    def test_login_fails_with_invalid_password(self, auth_service: AuthService):
        """Verify login fails with 400 when invalid password is provided."""
        response = auth_service.login(
            username=settings.AUTH_USERNAME,
            password="incorrect_password_123",
        )

        assert response.status == 400, f"Expected 400 Bad Request, got {response.status}"
        assert response.ok is False
        error_data = AuthErrorResponse.model_validate(response.json())
        assert "Invalid credentials" in error_data.message

    def test_login_fails_with_unknown_user(self, auth_service: AuthService):
        """Verify login fails with 400 for non-existent username."""
        fake_creds = generate_fake_credentials()
        response = auth_service.login(
            username=fake_creds["username"],
            password=fake_creds["password"],
        )

        assert response.status == 400
        error_data = AuthErrorResponse.model_validate(response.json())
        assert "Invalid credentials" in error_data.message

    def test_get_current_user_with_valid_token(self, auth_service: AuthService, session_auth_token: str):
        """Verify accessing /auth/me with valid Bearer token returns 200 and authenticated profile."""
        response = auth_service.get_current_user(token=session_auth_token)

        assert response.status == 200
        user_info = CurrentUserResponse.model_validate(response.json())
        assert user_info.username == settings.AUTH_USERNAME
        assert user_info.id == 1

    def test_get_current_user_without_token_is_unauthorized(self, auth_service: AuthService):
        """Verify accessing /auth/me without token returns 401 Unauthorized."""
        response = auth_service.get_current_user(token=None)

        assert response.status == 401
        assert "Access Token is required" in response.text()

    def test_get_current_user_with_invalid_token_is_rejected(self, auth_service: AuthService):
        """Verify accessing /auth/me with bogus token is rejected with 401 Unauthorized."""
        response = auth_service.get_current_user(token="invalid.bogus.jwt.token")

        assert response.status == 401
