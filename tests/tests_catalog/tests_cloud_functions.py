from .tests_catalogbase import TestCatalogBase
from flask import current_app

import requests
from datetime import datetime

from cloud_functions.cloud_tools import (
    get_cloud_function_url,
    generate_jwt_header,
    generate_jwt_access_token,
)


class TestCloudFunctions(TestCatalogBase):
    """
    This class tests the get functions from the cloud functions
    """

    # *** Get game by id tests ***

    def test_get_games_by_id_with_invalid_id_returns_a_valid_error(self):

        """
        Test the api response when the game_id is invalid(e.g: not a number)
        """

        get_games_by_id_url = get_cloud_function_url("get_game_by_id")

        response = requests.get(
            get_games_by_id_url, params={"game_id": "invalid_id"}
        ).json()

        self.assertEqual(response["message"], "Invalid game_id")
        self.assertEqual(response["status_code"], 400)

    def test_get_game_by_id_with_valid_id_returns_a_game(self):

        """
        Test the api response when the game_id is valid
        """

        get_games_by_id_url = get_cloud_function_url("get_game_by_id")

        response = requests.get(get_games_by_id_url, params={"game_id": 2}).json()

        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["data"][0]["game_id"], 2)

    def test_get_game_by_id_with_an_id_that_does_not_exist_returns_a_valid_error(
        self,
    ):

        """
        Test the api response when the game_id does not exist
        """

        get_games_by_id_url = get_cloud_function_url("get_game_by_id")

        response = requests.get(
            get_games_by_id_url, params={"game_id": "99999999"}
        ).json()

        self.assertEqual(response["message"], "No game found")
        self.assertEqual(response["status_code"], 404)
        self.assertEqual(response["data"], [])
        self.assertEqual(response["request_params"], {"game_id": "99999999"})

    # *** Get games by tags tests ***
    def test_get_games_by_tags_without_tags_returns_all_games(self):

        """
        Test the api response when the tags are not provided
        """

        get_games_by_tags_url = get_cloud_function_url("get_game_by_tags")

        response = requests.get(get_games_by_tags_url).json()

        self.assertEqual(response["status_code"], 200)
        self.assertNotEqual(response["data"], [])

    def test_get_games_by_tags_with_invalid_tags_returns_a_valid_response(
        self,
    ):

        """
        Check if the api response is valid when the tags are invalid
        is expected to return all games
        """

        get_games_by_tags_url = get_cloud_function_url("get_game_by_tags")

        response = requests.get(
            get_games_by_tags_url, params={"tags": "invalid_tag"}
        ).json()

        self.assertEqual(response["status_code"], 200)
        self.assertNotEqual(response["data"], [])

    def test_get_games_by_tags_with_valid_tags_returns_a_valid_response(self):

        """
        Check if the api response is valid when the tags are valid
        """

        get_games_by_tags_url = get_cloud_function_url("get_game_by_tags")

        response = requests.get(get_games_by_tags_url, params={"tags": "action"}).json()

        self.assertEqual(response["status_code"], 200)
        self.assertNotEqual(response["data"], [])

    def test_get_games_by_id_with_limit_parameter(self):

        """
        Check if the api response is valid when the limit parameter is provided
        """

        get_games_by_tags_url = get_cloud_function_url("get_game_by_tags")

        response = requests.get(
            get_games_by_tags_url, params={"tags": "Offline", "limit": 2}
        ).json()

        self.assertEqual(response["status_code"], 200)
        self.assertEqual(len(response["data"]), 2)

    def test_get_games_by_tags_with_start_at_parameter(self):

        """
        Check if the api response is valid when the start_at parameter is provided
        """

        get_games_by_tags_url = get_cloud_function_url("get_game_by_tags")

        response = requests.get(
            get_games_by_tags_url, params={"tags": "Offline", "start_at": 2}
        ).json()

        self.assertEqual(response["status_code"], 200)
        self.assertNotEqual(response["data"], [])

    # *** Edit game tests ***

    def test_edit_game_without_a_valid_token_returns_a_valid_error(self):

        """
        Test the api response when the token is invalid
        """

        edit_game_url = get_cloud_function_url("edit_game_by_id")

        response = requests.post(edit_game_url, json={}).json()

        self.assertEqual(response["message"], "Invalid token")
        self.assertEqual(response["status_code"], 401)

    def test_edit_game_with_a_expired_token_returns_a_valid_error(self):

        """
        Test the api response when the token is expired
        """

        edit_game_url = get_cloud_function_url("edit_game_by_id")

        payload = {
            "user_id": "1",
            "exp": datetime.now().timestamp() - 1000,
            "iat": datetime.now().timestamp(),
        }
        token = generate_jwt_access_token(payload)
        header = generate_jwt_header(token)

        response = requests.put(edit_game_url, json={}, headers=header).json()

        self.assertEqual(response["message"], "Invalid token")
        self.assertEqual(response["status_code"], 401)

    def test_edit_game_with_a_valid_token_and_invalid_game_id_returns_a_valid_error(
        self,
    ):

        # """
        # Test the api response when the token is valid and the game_id is invalid
        # """

        # edit_game_url = get_cloud_function_url("edit_game_by_id")

        # payload = {
        #     "user_id": "1",
        #     "exp": datetime.now().timestamp() + 1000,
        #     "iat": datetime.now().timestamp(),
        #     "data_to_edit": {"name": "test"},
        # }
        # token = generate_jwt_access_token(payload)
        # header = generate_jwt_header(token)

        # response = requests.put(
        #     edit_game_url, params={"game_id": "invalid"}, headers=header
        # ).json()

        # self.assertEqual(response["message"], "Invalid token")
        # self.assertEqual(response["status_code"], 401)
        # self.assertEqual(response["data"], None)
        pass

    def test_edit_game_with_a_valid_token_and_valid_game_id_and_no_data_to_edit_returns_a_valid_error(
        self,
    ):

        # """
        # Test the api response when the token is valid and the game_id is valid and the data_to_edit is None
        # """

        # edit_game_url = get_cloud_function_url("edit_game_by_id")

        # payload = {
        #     "user_id": "1",
        #     "exp": datetime.now().timestamp() + 1000,
        #     "iat": datetime.now().timestamp(),
        # }
        # token = generate_jwt_access_token(payload)
        # header = generate_jwt_header(token)

        # response = requests.put(
        #     edit_game_url, params={"game_id": "1"}, headers=header
        # ).json()

        # self.assertEqual(
        #     response["message"], "No json data was passed or invalid json data"
        # )
        # self.assertEqual(response["status_code"], 400)
        pass

    def test_edit_game_with_a_invalid_access_token(self):

        """
        Test the api response when the token is invalid
        """

        edit_game_url = get_cloud_function_url("edit_game_by_id")

        payload = {
            "user_id": "1",
            "exp": datetime.now().timestamp() + 1000,
            "iat": datetime.now().timestamp(),
            "data_to_edit": {"name": "test"},
        }

        token = "invalid_token"
        header = generate_jwt_header(token)

        response = requests.put(
            edit_game_url, params={"game_id": "2"}, headers=header
        ).json()

        self.assertEqual(response["message"], "Invalid token")
        self.assertEqual(response["status_code"], 401)

    # *** Create game tests ***

    def test_create_game_without_a_valid_token_returns_a_valid_error(self):

        """
        Test the api response when the token is invalid
        """

        create_game_url = get_cloud_function_url("create_game")

        response = requests.post(create_game_url, json={}).json()

        self.assertEqual(response["message"], "Invalid token")
        self.assertEqual(response["status_code"], 401)

    def test_create_game_with_a_expired_token_returns_a_valid_error(self):

        """
        Test the api response when the token is expired
        """

        create_game_url = get_cloud_function_url("create_game")

        payload = {
            "user_id": "1",
            "exp": datetime.now().timestamp() - 1000,
            "iat": datetime.now().timestamp(),
        }
        token = generate_jwt_access_token(payload)
        header = generate_jwt_header(token)

        response = requests.post(create_game_url, json={}, headers=header).json()

        self.assertEqual(response["message"], "Invalid token")
        self.assertEqual(response["status_code"], 401)
