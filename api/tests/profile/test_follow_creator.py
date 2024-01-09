
import allure
import pytest

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema, ProfileTestData as data

"""
Bug Report: BJT-132

Description:
- The API method 'follow_user' in the Profile API raises a concern. It's unclear if following regular users is intended or a bug.
- Current requirements do not specify that following should be exclusively for content creators.
- However, the Swagger UI description "Follow creator profile" implies it should be limited to creator profiles.

Note: 
- Once resolved, tests related to this functionality will be updated accordingly.
- test to update: test_follow_common_user
"""

class PreTestSetUpFollow:
    """
       The `PreTestSetUp` class is responsible for preparing the environment before the actual tests are executed.
       It ensures that the required state is set for the tests that follow. This setup is crucial for tests that
       assume certain conditions are already met.
       """
    def test_unfollow_creator(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        valid_data = {
            "creator_profile_id": data.other_creator_profile_id
        }
        profile_api.unfollow_user(valid_data)
@allure.feature("Start to follow creator")
@allure.severity("Major")
class TestFollowCreator:


    def test_follow_creator_profile_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        valid_data = {
            "creator_profile_id": data.other_creator_profile_id
        }
        response_body, status_code = profile_api.follow_user(valid_data)
        success_message = response_body.get("message")

        assert status_code == 200, f"Failed to follow creator, got {status_code} code"
        assert success_message == "Successfully followed"

    def test_repeated_follow_same_creator_negative(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        valid_data = {
            "creator_profile_id": data.other_creator_profile_id
        }
        response_body, status_code = profile_api.follow_user(valid_data)
        error_message = response_body.get("message")

        assert status_code == 400, f"Expected 400 for repeated following, got {status_code} instead"
        assert error_message == "You already follow this user"


    @pytest.mark.xfail
    def test_follow_common_user_negative(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        valid_data_common_user = {
            "creator_profile_id": data.other_common_user_profile_id
        }
        response_body, status_code = profile_api.follow_user(valid_data_common_user)
        print(response_body)
        #there is a bug: i can follow regular user (non creator)
        assert status_code == 400

    def test_follow_yourself_negative(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        current_user_profile_id = user_logged_in_session_fixture[3]
        data_with_current_user_profile_id = {
            "creator_profile_id": current_user_profile_id
        }
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.follow_user(data_with_current_user_profile_id)
        error_message = response_body["detail"]

        assert status_code == 400, f"Expected 400 for following yourself, got {status_code} instead"
        assert error_message == "Can't follow yourself"

    @pytest.mark.parametrize("request_data", [
        {"creator_profile_id": ""},
        {"": data.other_creator_profile_id},
        {"creator_profile_id": "abc"},
        {"abc": data.other_creator_profile_id},
        {"creator_profile_id": 123},
        {123: data.other_creator_profile_id},
    ])
    def test_follow_creator_with_invalid_format_user_profile_id_negative(self, user_logged_in_session_fixture, request_data):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.follow_user(request_data)

        assert status_code == 422, f"Expected 422 invalid values, got {status_code} instead"

    @pytest.mark.parametrize("request_data", [
        {"creator_profile_id": None},
        {None: data.other_creator_profile_id},
        {None: None},
    ])
    def test_follow_creator_with_empty_values_in_request_body_negative(self, user_logged_in_session_fixture, request_data):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.follow_user(request_data)
        error_message = response_body["detail"][0]["msg"]

        assert status_code == 422, f"Expected 422 for empty values, got {status_code} instead"
        assert error_message == "field required"

    def test_follow_creator_with_empty_request_body_negative(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        empty_request_body = data.empty_request_body
        response_body, status_code = profile_api.follow_user(empty_request_body)
        error_message = response_body["detail"][0]["msg"]

        assert status_code == 422, f"Expected 422 for empty request, got {status_code} instead"
        assert error_message == "field required"

    def test_follow_creator_with_non_existing_user_profile_id_negative(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        data_non_existing_user_profile_id = {
            "creator_profile_id": data.non_existing_user_profile_id
        }
        response_body, status_code = profile_api.follow_user(data_non_existing_user_profile_id)
        error_message = response_body["message"]

        assert status_code == 400, f"Expected 400 for non existing user_profile_id, got {status_code} instead"
        assert error_message == 'Key profile_creator_id is not present in table "user_profile".'

    def test_follow_creator_unauthorized_negative(self, user_not_logged_in_session_fixture):
        unauthenticated_session = user_not_logged_in_session_fixture
        profile_api = Profile(unauthenticated_session)
        valid_data = {
            "creator_profile_id": data.other_creator_profile_id
        }
        response_body, status_code = profile_api.follow_user(valid_data)
        error_message = response_body["detail"]

        assert status_code == 401, f"Expected 401 for unauthorized user, got {status_code} instead"
        assert error_message == "Not authenticated"


















