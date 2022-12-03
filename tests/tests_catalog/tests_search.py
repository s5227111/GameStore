from .tests_catalogbase import TestCatalogBase
from flask import current_app


class TestSearch(TestCatalogBase):
    """
    Testing Class responsible for testing the search endpoint
    """

    def test_db_conn_without_api(self):
        """
        Test if api has connected successfully
        Use Mongodb's method .find.one() to check if any result is returned
        Otherwise, probably the api has not connected to the database e the remaining tests will fail
        This test does not use the api endpoint, but the .find.one() method
        """

        # Search for any game WITHOUT USING API endpoint
        game = current_app.mongo.cx["Catalog"]["games"].find_one()
        # Verify that the game exists
        self.assertIsNotNone(game)

    def test_get_all_games_invalid_params(self):
        """
        Testing the get_all_games endpoint with invalid params
        """
        response = self.client.get("/apis/catalogApi/getAllGames/?start_at=-1&limit=-1")

        # Testing if the response is valid
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status_code"], 200)
        self.assertEqual(response.json["message"], "Success")
        self.assertEqual(response.json["request_params"], {"start_at": -1, "limit": -1})

    def test_get_all_games_valid_params(self):
        """
        Testing the get_all_games endpoint with valid params
        """
        response = self.client.get("/apis/catalogApi/getAllGames/?start_at=0&limit=100")

        # Testing if the response is valid
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status_code"], 200)
        self.assertEqual(response.json["message"], "Success")
        self.assertEqual(response.json["request_params"], {"start_at": 0, "limit": 100})
        self.assertIsNotNone(obj=response.json["data"])
