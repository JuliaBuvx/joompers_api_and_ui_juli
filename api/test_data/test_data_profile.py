
class ProfileTestData:
    other_creator_profile_id = "500e8112-e2fb-446b-9de2-251cf491708d"
    other_common_user_profile_id = "aae58dd2-c9b9-4f7b-b653-3eedc97b5a09"
    non_existing_user_profile_id = "9fa85f64-5717-4562-b3fc-2c963f66afa6"
    instagram_id = "56c6b6ee-b9ba-47e9-bc07-9b562a3424af"
    twitter_id = "701ba986-69be-4cc2-9f2e-58f48395b105"
    facebook_id = "402cdbc1-ca9d-42b2-94d8-56062e133f39"
    youtube_id = "3d4c0d2b-95b4-444c-8b5e-e9cad5052d6d"
    instagram_example_link = "http:"
    twitter_example_link = "http:"
    youtube_example_link = "http:"
    facebook_example_link = "http:"
    non_existing_social_network_id = "1d4c0d2b-95b4-444c-8b5e-e9cad5052d6d"
    profession_id_books = "a37eb0fb-2e32-4b71-af2d-c84f0fd204a9"
    profession_id_music = "fba72428-aaba-48ba-86ae-9ae2ced13e5e"
    valid_username_pattern = "max"
    non_existing_username_pattern = "uyrewoepowhbjf_333_99"
    valid_country = {"country": "France"}


    update_profile_full_valid_data = {
        "country": "United Kingdom",
        "name": "new",
        "username": "newusere123456",
        "sex": "Female",
        "bio": "string2",
        "professionId": "a37eb0fb-2e32-4b71-af2d-c84f0fd204a9",
        "photoUrl": None,
        "backgroundPictureUrl": None,
        "chatMessageNotify": False
    }
    update_profile_empty_values = {

        "country": None,
        "name": None,
        "username": None,
        "sex": None,
        "bio": None,
        "professionId": None,
        "photoUrl": None,
        "backgroundPictureUrl": None,
        "chatMessageNotify": None
    }

    empty_request_body = {
    }

class ProfileJsonSchemas:
    @staticmethod
    def get_followers_response_schema_success():
        return {
            "type": "object",
            "properties": {
                "profiles": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "userId": {"type": "string"},
                            "name": {"type": "string"},
                            "username": {"type": "string"},
                            "photoUrl": {"type": ["string", "null"]},
                            "bio": {"type": ["string", "null"]},
                            "role": {"type": "string"}
                        },
                        "required": ["id", "userId", "name", "username", "role"]
                    }
                },
                "count": {"type": "integer"}
            },
            "required": ["profiles", "count"]
        }
    @staticmethod
    def validation_error():
        return {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "loc": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "msg": {
                                    "type": "string"
                                },
                                "type": {
                                    "type": "string"
                                }
                            },
                            "required": ["loc", "msg", "type"]
                        }
                    }
                },
                "required": ["detail"]
            }

    @staticmethod
    def not_found_error():
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string"
                },
                "message": {
                    "type": "string"
                }
            },
            "required": ["code", "message"]
        }


    @staticmethod
    def get_followings_response_schema_success():
        return {
            "type": "object",
            "properties": {
                "profiles": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "userId": {"type": "string"},
                            "name": {"type": "string"},
                            "username": {"type": "string"},
                            "photoUrl": {"type": "string"},
                            "bio": {"type": "string"}
                        },
                        "required": ["id", "userId", "name", "username", "photoUrl", "bio"]
                    }
                },
                "count": {"type": "integer"}
            },
            "required": ["profiles", "count"]
        }
    @staticmethod
    def get_profile_by_username_response():
        return {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "userId": {"type": "string"},
                        "name": {"type": "string"},
                        "username": {"type": "string"},
                        "photoUrl": {"type": ["string", "null"]}
                    },
                    "required": ["id", "userId", "name", "username"]
                }
            }


    @staticmethod
    def get_settings_response_schema_success():
        return {
            "type": "object",
            "properties": {
                "country": {
                    "type": ["string", "null"]
                },
                "email": {
                    "type": "string",
                    "format": "email"
                },
                "sex": {
                    "type": ["string", "null"]
                },
                "profession": {
                    "type": ["string", "null"]
                },
                "chatMessageNotify": {
                    "type": "boolean"
                },
                "allCountries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "value": {
                                "type": "string"
                            },
                            "label": {
                                "type": "string"
                            }
                        },
                        "required": ["value", "label"]
                    }
                }
            },
            "required": ["email", "chatMessageNotify"]
        }

    @staticmethod
    def get_profile_creator_response_schema_success():
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid"
                },
                "userId": {
                    "type": "string",
                    "format": "uuid"
                },
                "name": {
                    "type": "string"
                },
                "username": {
                    "type": "string"
                },
                "photoUrl": {
                    "type": ["string", "null"]
                },
                "bio": {
                    "type": ["string", "null"]
                },
                "backgroundPictureUrl": {
                    "type": ["string", "null"]
                },
                "socialDataBlock": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "socialNetworkId": {
                                "type": "string",
                                "format": "uuid"
                            },
                            "socialNetworkIconUrl": {
                                "type": "string"
                            },
                            "socialNetworkTitle": {
                                "type": "string"
                            },
                            "socialNetworkUserValue": {
                                "type": ["string", "null"]
                            }
                        },
                        "required": ["socialNetworkId", "socialNetworkIconUrl", "socialNetworkTitle"]
                    }
                },
                "profession": {
                    "type": ["string", "null"]
                },
                "followers": {
                    "type": "integer"
                },
                "followings": {
                    "type": "integer"
                },
                "isFollowedByCurrentUser": {
                    "type": "boolean",
                },
                "isBlockedByCurrentUser": {
                    "type": "boolean"
                },
                "isBlockedByUser": {
                    "type": "boolean"
                }
            },
            "required": [
                "id",
                "userId",
                "name",
                "username",
                "socialDataBlock",
                "isBlockedByCurrentUser",
                "isBlockedByUser"
            ]
        }
    @staticmethod
    def get_profile_user_response_schema_success():
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "The unique identifier for the user profile."
                },
                "userId": {
                    "type": "string",
                    "format": "uuid",
                    "description": "The unique identifier for the user."
                },
                "name": {
                    "type": "string",
                    "description": "The name of the user."
                },
                "username": {
                    "type": "string",
                    "description": "The username for the user profile."
                },
                "photoUrl": {
                    "type": ["string", "null"],
                    "description": "The URL to the user's photo."
                },
                "isBlockedByCurrentUser": {
                    "type": "boolean",
                    "description": "Indicates if the user is blocked by the current user."
                },
                "isBlockedByUser": {
                    "type": "boolean",
                    "description": "Indicates if the user has been blocked by another user."
                }
            },
            "required": ["id", "userId", "name", "username"]
        }


