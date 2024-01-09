import requests
import allure


class Profile:

    def __init__(self, session):
        self.base_url = "https://api.dev.joompers.com"
        self.session = session
    def get_profile_followers(self, uuid, users_type, **kwargs):
        params = {'users_type': users_type}
        params.update(kwargs)
        response = self.session.get(
            f"{self.base_url}/api/profile/followers/{uuid}", params=params
        )
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {"error": "Failed to parse JSON response", "details": str(e)}
        return response_json, response.status_code
    def get_profile_followings(self, uuid):
        response = self.session.get(
            self.base_url + f"/api/profile/followings/{uuid}"
        )
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {"error": "Failed to parse JSON response", "details": str(e)}
        return response_json, response.status_code
    def get_user_status(self):
        response = self.session.get(
            self.base_url + "/api/profile/status"
        )
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {"error": "Failed to parse JSON response", "details": str(e)}
        return response_json, response.status_code
    def get_profile_settings(self):
        response = self.session.get(
            self.base_url + "/api/profile/settings"
        )
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {"error": "Failed to parse JSON response", "details": str(e)}
        return response_json, response.status_code
    def get_profile_by_username_pattern(self, **kwargs):
        params = {
        }
        params.update(kwargs)
        response = self.session.get(
            f"{self.base_url}/api/profile/get_by_username_pattern", params=params
        )
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {"error": "Failed to parse JSON response", "details": str(e)}
        return response_json, response.status_code
    def get_profile(self, uuid):
        response = self.session.get(
            self.base_url + f"/api/profile/{uuid}"
        )
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {"error": "Failed to parse JSON response", "details": str(e)}
        return response_json, response.status_code
    def follow_user(self, data):
        response = self.session.post(url=
            self.base_url + "/api/profile/follow", json=data
        )
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {"error": "Failed to parse JSON response", "details": str(e)}
        return response_json, response.status_code
    def unfollow_user(self, data):

        response = self.session.post(url=
                                     self.base_url + "/api/profile/unfollow", json=data
                                     )
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {"error": "Failed to parse JSON response", "details": str(e)}
        return response_json, response.status_code
    def remove_follower(self, data):
        response = self.session.post(url=
                                     self.base_url + "/api/profile/remove_follower", params=data
                                     )
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {"error": "Failed to parse JSON response", "details": str(e)}
        return response_json, response.status_code
    def change_social_network(self, data):
        response = self.session.post(
            self.base_url + "/api/profile/change_social_network", json=data
        )
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {"error": "Failed to parse JSON response", "details": str(e)}
        return response_json, response.status_code
    def update_profile(self, data):
        response = self.session.patch(
            self.base_url + "/api/profile/update", json=data
        )
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {"error": "Failed to parse JSON response", "details": str(e)}
        return response_json, response.status_code