import allure
import jsonschema
import pytest
from jsonschema import validate

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema, ProfileTestData as data


@allure.feature("Get profile by username")
@allure.severity("Normal")
class TestGetProfileByUsername:
    def test_get_profile_by_username_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        valid_pattern = data.valid_username_pattern
        response_body, status_code = profile_api.get_profile_by_username_pattern(pattern=valid_pattern)

        assert status_code == 200, "Failed to get user profile by username"
        try:
            validate(instance=response_body, schema=schema.get_profile_by_username_response())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    @pytest.mark.parametrize("limit, offset", [
        (1, 0),
        (0, 1),
        (999, 0),
        (1000, 0),
        (10, 1000)
    ])
    def test_get_profile_by_username_with_limit_and_offset_positive(self, user_logged_in_session_fixture, limit, offset):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        valid_pattern = data.valid_username_pattern
        response_body, status_code = profile_api.get_profile_by_username_pattern(pattern=valid_pattern,
                                                                                 limit=limit, offset=offset)

        assert status_code == 200, "Failed to get user profile by username"
        try:
            validate(instance=response_body, schema=schema.get_profile_by_username_response())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"
        assert len(response_body) <= limit, f"Returned more profiles than the limit of {limit}"

    @pytest.mark.parametrize("limit, offset", [
        (1001, -1),
        (10, -1),
        (-1, 10),
        (10, "ten"),
        ("ten", 10),
        (10, "^$#>/"),
        ("^$#>/", 10),
        (10, ""),
        ("", 10),
    ])
    def test_get_profile_by_username_with_invalid_limit_and_offset_negative(self, user_logged_in_session_fixture, limit, offset):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        valid_pattern = data.valid_username_pattern
        response_body, status_code = profile_api.get_profile_by_username_pattern(pattern=valid_pattern,
                                                                                 limit=limit, offset=offset)

        assert status_code == 422, f"Expected 422 for invalid parameters, got {status_code} instead"


    def test_get_profile_by_username_non_existing_username_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        non_existing_pattern = data.non_existing_username_pattern
        response_body, status_code = profile_api.get_profile_by_username_pattern(pattern=non_existing_pattern)

        assert status_code == 200, "Failed to get user profile by username"
        assert response_body == []

    def test_get_profile_by_username_unauthorized_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        valid_pattern = data.valid_username_pattern
        response_body, status_code = profile_api.get_profile_by_username_pattern(pattern=valid_pattern)

        assert status_code == 200, "Failed to get user profile by username"
        try:
            validate(instance=response_body, schema=schema.get_profile_by_username_response())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"



