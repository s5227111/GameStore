from flask_pymongo import PyMongo, ObjectId

# Import of utilitaries
from typing import Union, Optional
from dataclasses import dataclass, asdict

# Command used only for MacOs, should not be used in production
import certifi

ca = certifi.where()


class MissingRequiredField(Exception):
    """
    Exception raised when a required field is missing
    """


@dataclass
class Game:
    """
    Represents a game from the businee logic perspective
    Also responsible for the data validation

    !!! ATTENTION !!!
    Disambiguity: the field _id is not our id but the MongoDB id
    Always use the "game_id" field to refer to our id of our application

    Parameters
    ----------

    _id: Union[str, ObjectId]
    game_id: str - Game id
    name: str - Game name
    short_description: str - Game short description

    pricing: object
        listed_price: float - Game listed price
        discount_percentage: float - Game discount percentage
        final_price: float - Game final price

    !!! ATTENTION !!!
    # TODO: implement business logic
    # Temporaly set as optional
    attributes: object (optional)
        minimum_players: int - Game minimum players
        maximum_players: int - Game maximum players
        minimum_playtime: int - Game minimum playtime
        maximum_playtime: int - Game maximum playtime
        minimum_age: int - Game minimum age

    images: object (optional)
        cover: str - Game cover image
        gallery: list - Game gallery images

    reviews: object (required)
        total: int - Total reviews
        positive: int - Positive reviews
        negative: int - Negative reviews
        percentage_positive: float - Percentage of positive reviews
        percentage_negative: float - Percentage of negative reviews
        comments: list - Game comments

    """

    _id: Union[str, ObjectId]
    game_id: str
    name: str
    short_description: str

    pricing: object

    attributes: Optional[object] = None
    reviews: Optional[object] = None
    images: Optional[object] = None

    def __post_init__(self) -> None:
        """
        Validate data and convert ObjectId to string
        """

        self.__convert_objectId_to_str()
        self.__check_required_fields()

    def __convert_objectId_to_str(self) -> None:
        """
        Convert the ObjectId (Mongo) to a string because the ObjectId is not JSON serializable

        :return: None
        """
        self._id = str(self._id)

    def __check_required_fields(self) -> bool:
        """
        Check if all required fields are present

        :return: bool
        """
        required_fields = [
            "_id",
            "game_id",
            "name",
            "short_description",
            "pricing",
        ]

        for field in required_fields:
            if not hasattr(self, field):
                raise MissingRequiredField(f"Missing required field: {field}")

        return True

    def to_dict(self) -> dict:
        """
        Convert the object to a dictionary
        """
        return {k: v for k, v in asdict(self).items() if v is not None}


class GameCollectionQuery:
    """
    Class responsible for querying the game collection
    """

    @staticmethod
    def get_all_products(start_at: int, limit: int) -> list:
        """
        Get all games from the game collection

        :param start_at: int - number of products (json's documents) to skip
        :param limit: int - number of products (json's documents) to return
        :return: list


        ! OBSERVATIONS !
        If start_at is bigger than the number of documents in the collection, the query will return an empty list
        If the pagination is invalid, the query will return an empty list
        """

        collection = mongo.cx["Catalog"]["games"]
        result = collection.find().skip(start_at).limit(limit)
        result = [Game(**game) for game in result]
        return result


mongo = PyMongo()


def configure(app, test_mode=False):
    if test_mode:
        app.config[
            "MONGO_URI"
        ] = "mongodb+srv://root:1234@cluster0.gg84ero.mongodb.net/?retryWrites=true&w=majority"
    else:
        app.config[
            "MONGO_URI"
        ] = "mongodb+srv://root:1234@cluster0.gg84ero.mongodb.net/?retryWrites=true&w=majority"

    mongo.init_app(app)
    app.mongo = mongo
