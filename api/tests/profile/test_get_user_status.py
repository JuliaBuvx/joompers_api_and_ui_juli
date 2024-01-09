import allure
import pytest

from api.api_library.profile import Profile
from api.conftest import user_logged_in_session_fixture


class TestGetUserStatus:
    @allure.feature("Get user current status")
    @allure.severity('Major')
    def test_get_user_status_success_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)

        response_body, status = profile_api.get_user_status()
        assert status == 200
        assert response_body == "active"

    def test_get_user_status_unauthenticated_negative(self, user_not_logged_in_session_fixture):
        unauthenticated_session = user_not_logged_in_session_fixture
        profile_api = Profile(unauthenticated_session)
        response_body, status = profile_api.get_user_status()
        error_message = response_body["detail"]

        assert status == 401, f"Expected 401 for unauthorized user, got {status} instead"
        assert error_message == "Not authenticated"


