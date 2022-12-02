from .tests_catalogbase import TestCatalogBase


class TestSearch(TestCatalogBase):
    """
    Testing Class responsible for testing the search endpoint
    """

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
