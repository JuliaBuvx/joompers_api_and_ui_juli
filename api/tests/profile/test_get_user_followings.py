import allure
import jsonschema
import pytest
from jsonschema import validate

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema, ProfileTestData as data

"""
Bug Report: BJT-159

159: an issue was identified where the "photoUrl" value may be absent (set to None), 
but the schema requires this value to be a string. 

Note: 
- Once resolved, tests related to this functionality will be updated accordingly.
"""

@allure.feature("Get user followings list")
@allure.severity("Normal")
class TestGetUserFollowings:

    @pytest.mark.xfail
    def test_get_own_followings_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        user_profile_id = user_logged_in_session_fixture[3]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.get_profile_followings(user_profile_id)

        assert status_code == 200, "Failed to get user followings"
        try:
            validate(instance=response_body, schema=schema.get_followings_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    @pytest.mark.xfail
    def test_get_other_user_followings_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        user_profile_id = data.other_creator_profile_id
        response_body, status_code = profile_api.get_profile_followings(user_profile_id)

        assert status_code == 200, "Failed to get user followings"
        try:
            validate(instance=response_body, schema=schema.get_followings_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"
    def test_get_user_followings_with_non_existing_user_profile_id_negative(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        user_profile_id = data.non_existing_user_profile_id
        response_body, status_code = profile_api.get_profile_followings(user_profile_id)
        error_message = response_body.get("message")

        assert status_code == 404, f"Expected 404 for non existing user_profile_id, got {status_code} instead"
        assert error_message == "User was not found"

    @pytest.mark.parametrize("user_profile_id", [
        "abc",
        123,
        "",
        None
    ]
    )
    def test_get_user_followings_with_invalid_format_user_profile_id_negative(self, user_logged_in_session_fixture, user_profile_id):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.get_profile_followings(user_profile_id)
        error_message = response_body["detail"][0]["msg"]

        assert status_code == 422, f"Expected 422 for invalid parameters, got {status_code} instead"
        assert error_message == "value is not a valid uuid"

    @pytest.mark.xfail
    def test_get_user_followings_unauthorized_positive(self, user_not_logged_in_session_fixture):
        unauthenticated_session = user_not_logged_in_session_fixture
        profile_api = Profile(unauthenticated_session)
        user_profile_id = data.other_creator_profile_id
        response_body, status_code = profile_api.get_profile_followings(user_profile_id)

        assert status_code == 200, f"Expected 200 for unauthorized user, got {status_code} instead"
        try:
            validate(instance=response_body, schema=schema.get_followings_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"


