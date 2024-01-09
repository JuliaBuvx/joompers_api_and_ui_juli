import allure
import jsonschema
import pytest
from jsonschema import validate

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema, ProfileTestData as data


"""
Bug Report: BJT-141

Description:
- Lack of URL Validation in change Social Network API.
- The /api/profile/change_social_network API accepts invalid URLs in the social_network_user_value field
- Server-side URL format validation is required to prevent such issues.

Note: 
- Once resolved, tests related to this functionality will be updated accordingly.
- test to update: test_add_network_with_invalid_values_in_request_body
"""

class TestChangeSocialNetwork:
    @pytest.mark.parametrize("social_network_id, social_network_link", [
        (data.youtube_id, data.youtube_example_link),
        (data.instagram_id, data.instagram_example_link),
        (data.facebook_id, data.facebook_example_link),
        (data.twitter_id, data.twitter_example_link)
    ])
    def test_add_social_network_to_profile_positive(self, user_logged_in_session_fixture, social_network_id,
                                                      social_network_link):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        valid_data = {
            "social_network_id": social_network_id,
            "social_network_user_value": social_network_link
        }
        response_body, status_code = profile_api.change_social_network(valid_data)
        success_message = response_body.get("message")

        assert status_code == 200, f"Failed to add social network, got {status_code} code"
        assert success_message == "Successfully added social network", f"Got {success_message} instead"

    @pytest.mark.parametrize("social_network_id, social_network_link", [
        (data.twitter_id, None),
        (None, data.twitter_example_link),
        (None, None)
    ])
    def test_add_social_network_with_empty_values_in_request_body_negative(self, user_logged_in_session_fixture, social_network_id, social_network_link):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        data_with_empty_values = {
            "social_network_id": social_network_id,
            "social_network_user_value": social_network_link
        }
        response_body, status_code = profile_api.change_social_network(data_with_empty_values)
        error_message = response_body["detail"][0]["msg"]

        assert status_code == 422, f"Expected 422 for invalid value, got {status_code} code instead"
        assert error_message == "field required"

    def test_add_social_network_with_empty_request_body_negative(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        empty_request_body = data.empty_request_body
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.change_social_network(empty_request_body)
        error_message = response_body["detail"][0]["msg"]

        assert status_code == 422, f"Failed to add social network, got {status_code} code"
        assert error_message == "field required"

    @pytest.mark.xfail
    @pytest.mark.parametrize("social_network_id, social_network_link, expected_error_msg", [
        ("some string", data.twitter_example_link, "value is not a valid url"),
        (data.twitter_id, "some string", "value is not a valid url"),
        ("", data.twitter_example_link, "field required"),
        (data.twitter_id, "", "field required"),
        (123, data.twitter_example_link, "value is not a valid url"),
        (data.twitter_id, 123, "value is not a valid url"),
    ])
    def test_add_network_with_invalid_values_in_request_body_negative(self, user_logged_in_session_fixture, social_network_id,
                                                      social_network_link, expected_error_msg):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        invalid_data = {
            "social_network_id": social_network_id,
            "social_network_user_value": social_network_link
        }
        response_body, status_code = profile_api.change_social_network(invalid_data)

        assert status_code == 422, f"Expected 422 for invalid parameters, got {status_code} instead"
        error_message = response_body["detail"][0]["msg"]
        assert error_message == expected_error_msg

    def test_add_network_with_non_existing_social_network_id_negative(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        non_existing_data = {
            "social_network_id": data.non_existing_social_network_id,
            "social_network_user_value": data.twitter_example_link
        }
        response_body, status_code = profile_api.change_social_network(non_existing_data)
        error_message = response_body["message"]

        assert status_code == 400, f"Expected 400 for non existing user_profile_id, got {status_code} instead"
        assert error_message == "Social network was not found"

    def test_add_social_network_unauthorized_negative(self, user_not_logged_in_session_fixture):
        unauthenticated_session = user_not_logged_in_session_fixture
        profile_api = Profile(unauthenticated_session)
        valid_data = {
            "social_network_id": data.twitter_id,
            "social_network_user_value": data.twitter_example_link
        }
        response_body, status_code = profile_api.change_social_network(valid_data)
        error_message = response_body["detail"]

        assert status_code == 401, f"Expected 401 for unauthorized user, got {status_code} instead"
        assert error_message == "Not authenticated"

