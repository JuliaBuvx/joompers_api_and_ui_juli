import allure
import pytest

from api.api_library.profile import Profile
from api.test_data.test_data_profile import ProfileJsonSchemas as schema, ProfileTestData as data
"""
Bug Report: BJT-154, 156, 157

Note: 
- There are many bugs and ambiguities here, so the tests will be revised later.
- there is no max value for bio
- 200 for an empty 'country' field and an empty 'bio' (if 'None'). 500 for an empty 'name' field (if 'None'). 
It looks like an inconsistency in handling empty fields.

- Username must contain from 3 to 32 symbols (numbers, letters or '.' are allowed),
- Sex Must be Male, Female or Other'

"""
@allure.feature("Update profile")
@allure.severity("Normal")
class TestUpdateProfile:

    def test_update_profile_country_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        valid_data = data.valid_country
        response_body, status_code = profile_api.update_profile(data=valid_data)
        assert status_code == 200, f"Failed to update country, got {status_code} code"
        assert response_body.get("country") == valid_data["country"], "Country did not update correctly"

    @pytest.mark.parametrize("invalid_data", [
        {"country": "justastring"},
        {"country": "12345"},
        {"country": "!!@@##"},
        {"country": ""},
        {"country": None},
        {}
    ])
    def test_update_profile_country_negative(self, user_logged_in_session_fixture, invalid_data):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.update_profile(data=invalid_data)
        assert status_code == 400, f"Expected 400 for invalid data, got {status_code} code"

    @pytest.mark.parametrize("valid_names",[
        "New Name",
        "A",
        "AA",
        "B" * 100,
        "B" * 99,
    ])
    def test_update_profile_name_positive(self, user_logged_in_session_fixture, valid_names):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"name": valid_names}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update name, got {status_code} code"
        assert response_body.get("name") == valid_names, "Name did not update correctly"

    @pytest.mark.parametrize("invalid_data", [
        {"name": ""},
        {"name": " "},
        {"name": "B" * 101},
        {"name": 123},
        {"name": "Invalid_Name!"},
        {"name": None},
        {}
    ])
    def test_update_profile_name_negative(self, user_logged_in_session_fixture, invalid_data):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.update_profile(data=invalid_data)

        assert status_code == 422, f"Expected 422 for invalid data, got {status_code} code"

    @pytest.mark.parametrize("valid_data", [
        {"username": "newUserName12"},
        {"username": "ss"},
        {"username": "sss"},
        {"username": "s" * 31},
        {"username": "s" * 32},
    ])
    def test_update_profile_username_positive(self, user_logged_in_session_fixture, valid_data):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"username": "newUserName12"}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update username, got {status_code} code"
        assert response_body.get("username") == update_data["username"], "Username did not update correctly"

    @pytest.mark.parametrize("invalid_data", [
        {"username": "s"},
        {"username": "s" * 33},
        {"username": 123},
        {"username": None},
        {},
    ])
    def test_update_profile_username_negative(self, user_logged_in_session_fixture, invalid_data):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.update_profile(data=invalid_data)

        assert status_code == 422, f"Expected 422 for invalid data, got {status_code} code"

    @pytest.mark.parametrize("valid_data", [
        {"sex": "Female"},
        {"sex": "Male"},
        {"sex": "Other"},
    ])
    def test_update_profile_sex_positive(self, user_logged_in_session_fixture, valid_data):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.update_profile(data=valid_data)

        assert status_code == 200, f"Failed to update sex, got {status_code} code"
        assert response_body.get("sex") == valid_data["sex"], "Sex did not update correctly"

    @pytest.mark.parametrize("invalid_data", [
        {"sex": "string"},
        {"sex": 123},
        {"sex": None},
        {},
    ])
    def test_update_profile_sex_negative(self, user_logged_in_session_fixture, invalid_data):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.update_profile(data=invalid_data)

        assert status_code == 422, f"Expected 422 for invalid data, got {status_code} code"

    @pytest.mark.parametrize("valid_data", [
        {"bio": "new bio"},
        {"bio": "n" * 499},
        {"bio": "n" * 500},
    ])
    def test_update_profile_bio_positive(self, user_logged_in_session_fixture, valid_data):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.update_profile(data=valid_data)

        assert status_code == 200, f"Failed to update bio, got {status_code} code"
        assert response_body.get("bio") == valid_data["bio"], "Bio did not update correctly"

    @pytest.mark.parametrize("invalid_data", [
        {"bio": ""},
        {"bio": " "},
        {"bio": "A" * 501},
        {"bio": None},
        {}
    ])
    def test_update_profile_bio_negative(self, user_logged_in_session_fixture, invalid_data):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.update_profile(data=invalid_data)

        assert status_code == 422, f"Failed to update bio, got {status_code} code"

    def test_update_profile_profession_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"professionId": data.profession_id_music}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update professionId, got {status_code} code"
        assert response_body.get("professionId") == update_data["professionId"], "ProfessionId did not update correctly"

    @pytest.mark.xfail
    def test_update_profile_photo_url_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"photoUrl": "https://poroda-mops.ru/wp-content/uploads/2017/06/kak-pravilno-vybrat-shhenka-mopsa.jpg"}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update photoUrl, got {status_code} code"
        assert response_body.get("photoUrl") == update_data["photoUrl"], "photoUrl did not update correctly"

    @pytest.mark.xfail
    def test_update_profile_background_picture_url_positive(self, user_logged_in_session_fixture):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        update_data = {"backgroundPictureUrl": "https://vashkinolog.com/wp-content/uploads/2017/10/mopsiki_foto_shenki_1-360x270.jpg"}
        response_body, status_code = profile_api.update_profile(data=update_data)

        assert status_code == 200, f"Failed to update country, got {status_code} code"
        assert response_body.get("backgroundPictureUrl") == update_data["backgroundPictureUrl"], "backgroundPictureUrl did not update correctly"

    @pytest.mark.parametrize("valid_data", [
        {"chatMessageNotify": False},
        {"chatMessageNotify": True},
    ])
    def test_update_profile_chat_message_notify_positive(self, user_logged_in_session_fixture, valid_data):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.update_profile(data=valid_data)

        assert status_code == 200, f"Failed to update country, got {status_code} code"
        assert response_body.get("chatMessageNotify") == valid_data["chatMessageNotify"], "chatMessageNotify did not update correctly"

    @pytest.mark.parametrize("invalid_data", [
        {"chatMessageNotify": "False"},
        {"chatMessageNotify": 123},
        {"chatMessageNotify": ""},
        {"chatMessageNotify": None},
        {},
    ])
    def test_update_profile_chat_message_notify_negative(self, user_logged_in_session_fixture, invalid_data):
        authenticated_session = user_logged_in_session_fixture[0]
        profile_api = Profile(authenticated_session)
        response_body, status_code = profile_api.update_profile(data=invalid_data)

        assert status_code == 422, f"Expected 422 for invalid data, got {status_code} code"


    def test_update_profile_unauthorized_negative(self, user_not_logged_in_session_fixture):
        unauthenticated_session = user_not_logged_in_session_fixture
        profile_api = Profile(unauthenticated_session)
        update_data = {"country": "France"}
        response_body, status_code = profile_api.update_profile(data=update_data)
        error_message = response_body["detail"]

        assert status_code == 401, f"Expected 401 for unauthorized user, got {status_code} instead"
        assert error_message == "Not authenticated"

