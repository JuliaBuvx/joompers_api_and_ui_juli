import allure
import jsonschema
import pytest
from jsonschema import validate

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema, ProfileTestData as data
from api.conftest import user_logged_in_session_fixture
"""
Bug Report: BJT-121

Description:
- Incorrect value of "isBlockedByCurrentUser" for get_profile_unauthorized
- test to update: test_follow_creator_profile_unauthorized

"""

@allure.feature("Get user profile")
@allure.severity("Normal")
class TestGetProfile:
    def test_get_own_profile_successful_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        user_profile_id = user_logged_in_session_fixture[3]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.get_profile(user_profile_id)

        assert status_code == 200, "Failed to get user profile"
        try:
            any_of_schema = {
                "anyOf": [
                    schema.get_profile_creator_response_schema_success(),
                    schema.get_profile_user_response_schema_success()
                ]
            }
            validate(instance=response_body, schema=any_of_schema)
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    def test_get_other_user_profile_with_role_creator_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        user_profile_id = data.other_creator_profile_id
        response_body, status_code = profile_api.get_profile(user_profile_id)

        assert status_code == 200, "Failed to get user profile"
        try:
            validate(instance=response_body, schema= schema.get_profile_creator_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    def test_get_other_user_profile_for_role_common_user_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        user_profile_id = data.other_common_user_profile_id

        response_body, status_code = profile_api.get_profile(user_profile_id)
        assert status_code == 200, "Failed to get user profile"
        try:
            validate(instance=response_body, schema=schema.get_profile_user_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    def test_get_profile_with_non_existing_user_profile_id_negative(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        user_profile_id = data.non_existing_user_profile_id
        response_body, status_code = profile_api.get_profile(user_profile_id)
        error_message = response_body.get("message")

        assert status_code == 404, f"Expected 404 for non existing user_profile_id, got {status_code} instead"
        assert error_message == "User was not found"

    @pytest.mark.parametrize("user_profile_id", [
            "abc",
            123,
            None,
        ])
    def test_get_profile_with_invalid_format_user_profile_id_negative(self, user_logged_in_session_fixture, user_profile_id):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.get_profile(user_profile_id)
        error_message = response_body["detail"][0]["msg"]

        assert status_code == 422, f"Expected 422 for invalid parameters, got {status_code} instead"
        assert error_message == "value is not a valid uuid"
    @pytest.mark.xfail
    def test_get_user_profile_unauthorized_positive(self, user_not_logged_in_session_fixture):
        unauthenticated_session = user_not_logged_in_session_fixture
        profile_api = Profile(unauthenticated_session)
        user_profile_id = data.other_common_user_profile_id

        response_body, status_code = profile_api.get_profile(user_profile_id)
        assert status_code == 200, f"Expected 200 for unauthorized user, got {status_code} instead"
        #there is a minor bug in response json: non-required 'isBlockedByCurrentUser' can be true or false (not None)
        try:
            validate(instance=response_body, schema=schema.get_profile_creator_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"