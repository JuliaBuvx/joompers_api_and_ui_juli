import allure
import jsonschema
import pytest
from jsonschema import validate

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema, ProfileTestData as data

"""
Bug Report: BJT-121

Description:
When a request to retrieve a user profile is made by a user who is not authenticated, 
the isBlockedByCurrentUser field is returned with a value of None, 
whereas a boolean value (true or false) is expected.

Bug Report: BJT-119
Description: 200 ok response  for invalid query parameter user_type

Bug Report: BJT-132
Description:
- The API method 'follow_user' in the Profile API raises a concern. It's unclear if following regular users is intended or a bug.
- Current requirements do not specify that following should be exclusively for content creators.
- However, the Swagger UI description "Follow creator profile" implies it should be limited to creator profiles.

Note: 
- Once resolved, tests related to this functionality will be updated accordingly.
"""

@allure.feature("Get user followers list")
@allure.severity("Normal")
class TestGetUserFollowers:
    @pytest.mark.parametrize("user_type", [
        "author",
        "all",
        "user"
    ])
    def test_get_own_profile_followers_with_every_user_type_positive(self, user_logged_in_session_fixture, user_type):
        authenticated_session = user_logged_in_session_fixture[0]
        user_profile_id = user_logged_in_session_fixture[3]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.get_profile_followers(user_profile_id, user_type)

        assert status_code == 200, "Failed to get user followers"
        try:
            validate(instance=response_body, schema=schema.get_followers_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"

    def test_get_other_user_followers_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        user_profile_id = data.other_creator_profile_id
        profile_api = Profile(authenticated_session)
        user_type = "all"
        response_body, status_code = profile_api.get_profile_followers(user_profile_id, user_type)

        assert status_code == 200, "Failed to get user followers"
        try:
            validate(instance=response_body, schema=schema.get_followers_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"
    @pytest.mark.parametrize("limit, offset", [
        (1, 0),
        (0, 1),
        (999, 0),
        (1000, 0),
        (10, 1000)
    ])
    def test_get_user_followers_limit_and_offset_positive(self, user_logged_in_session_fixture, limit, offset):
        authenticated_session = user_logged_in_session_fixture[0]
        user_profile_id = user_logged_in_session_fixture[3]
        profile_api = Profile(authenticated_session)

        user_type = "all"
        response_body, status_code = profile_api.get_profile_followers(user_profile_id, user_type, limit=limit, offset=offset)

        assert status_code == 200, "Failed to get user followers"
        try:
            validate(instance=response_body, schema=schema.get_followers_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"
        assert len(response_body['profiles']) <= limit, f"Returned more profiles than the limit of {limit}"

    @pytest.mark.parametrize("user_type", [
        "somestring",
        "",
        123,
        "^$#>/"
    ])
    def test_get_user_followers_with_invalid_user_type_negative(self, user_logged_in_session_fixture, user_type):
        authenticated_session = user_logged_in_session_fixture[0]
        user_profile_id = user_logged_in_session_fixture[3]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.get_profile_followers(user_profile_id, user_type)
        error_message = response_body.get("detail")

        assert status_code == 400, f"Expected 400 for invalid parameters, got {status_code} instead"
        assert error_message == "Not available users_type (must be only author, user, all)"


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
    def test_get_user_followers_invalid_limit_and_offset_negative(self, user_logged_in_session_fixture, limit, offset):
        authenticated_session = user_logged_in_session_fixture[0]
        user_profile_id = user_logged_in_session_fixture[3]
        profile_api = Profile(authenticated_session)
        user_type = "all"
        response_body, status_code = profile_api.get_profile_followers(user_profile_id, user_type, limit=limit, offset=offset)

        assert status_code == 422, f"Expected 422 for invalid parameters, got {status_code} instead"

    def test_get_user_followers_with_non_existing_user_profile_id_negative(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        user_profile_id = data.non_existing_user_profile_id
        response_body, status_code = profile_api.get_profile_followers(user_profile_id, users_type="all")
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
    def test_get_user_followers_with_invalid_format_user_profile_id_negative(self, user_logged_in_session_fixture, user_profile_id):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.get_profile_followers(user_profile_id, users_type="all")
        error_message = response_body["detail"][0]["msg"]

        assert status_code == 422, f"Expected 422 for invalid parameters, got {status_code} instead"
        assert error_message == "value is not a valid uuid"

    def test_get_user_followers_unauthorized_positive(self, user_not_logged_in_session_fixture):
        unauthenticated_session = user_not_logged_in_session_fixture
        profile_api = Profile(unauthenticated_session)
        user_profile_id = data.other_creator_profile_id
        response_body, status_code = profile_api.get_profile_followers(user_profile_id, users_type="all")

        assert status_code == 200, f"Expected 200 for unauthorized user, got {status_code} instead"
        try:
            validate(instance=response_body, schema=schema.get_followers_response_schema_success())
        except jsonschema.exceptions.ValidationError as e:
            assert False, f"Response did not match schema: {e}"
