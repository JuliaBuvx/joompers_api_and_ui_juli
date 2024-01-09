import allure
import jsonschema
import pytest
from jsonschema import validate

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema
from api.conftest import user_logged_in_session_fixture

@allure.feature("Get user settings")
@allure.severity('Major')
class TestGetProfileSettings:
    def test_get_profile_settings_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.get_profile_settings()
        assert status_code == 200, "Failed to get user settings"
        try:
            validate(instance=response_body, schema=schema.get_settings_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    def test_get_profile_settings_unauthenticated_negative(self, user_not_logged_in_session_fixture):
        unauthenticated_session = user_not_logged_in_session_fixture
        profile_api = Profile(unauthenticated_session)
        response_body, status = profile_api.get_profile_settings()
        error_message = response_body["detail"]

        assert status == 401, f"Expected 401 for unauthorized user, got {status} instead"
        assert error_message == "Not authenticated"