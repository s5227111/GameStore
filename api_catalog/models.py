from flask_pymongo import PyMongo, ObjectId

# Import of utilitaries
from typing import Union, Optional
from dataclasses import dataclass, asdict

from .api_errors import MissingRequiredField, UnexpectedFieldError


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

    _id: Union[str, ObjectId] - for the business logic, the _id is the MongoDB id
    game_id: str - Game id
    name: str - Game name
    added_at: str - Game added date
    developer: str - Game developer
    downloads: int - Game downloads
    pricing: float - Game price
    tags: list - Game tags
    images: list - Game images
    details: dict - Game details
    reviews: object (required)

    !!! ATTENTION !!!
    Disambiguity: For business logic, the _id field will not be our id but the MongoDB id.
    We must always look for game_id to reference the game id of our application

    Also, _id is treated by the dataclass as an optional attribute, as MongoDB creates the ObjectId automatically
    when we need to insert a new game into the database. However, for business logic, the attribute
    _id is required as we need to know which game we are updating or deleting.
    In other words, the _id attribute is mandatory for business logic, but optional for MongoDB.
    Your searches like "update", "edit" and "delete" should start from the premise that the _id attribute is mandatory, while
    during the insertion of a new game, the _id attribute MUST NOT BE PASSED.

    The business model does not support the creation of new fields, that is, if MongoDB returns a field that is not
    defined in the class, an exception will be thrown.
    At the same time, the business model does not support the creation of empty fields, that is, if MongoDB returns a
    empty field, an exception will be thrown.
    Finally, if during the creation of a new game, some 'strange' field is passed, an exception will be thrown.
    This is done to ensure semi-structured data. Still, you can use additional fields in
    fields that are of type "dict" or "list". For example, it is possible to create a game by inserting the value 'colors': ['red', 'blue'],
    inside the details field. However, it is not possible to create a book by entering the value 'colors': ['red', 'blue'].

    """

    # _id: Union[str, ObjectId]
    game_id: int
    name: str
    added_at: str
    developer: str
    downloads: int
    pricing: float
    tags: list
    images: dict
    details: dict
    reviews: dict

    _id: Optional[Union[str, ObjectId]] = None

    # tags: Optional[list] = None

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
            "game_id",
            "name",
            "added_at",
            "developer",
            "downloads",
            "pricing",
            "images",
            "details",
            "reviews",
            "tags",
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

    def __eq__(self, __o: object) -> bool:
        """
        Check if the object is equal to another object
        """
        if isinstance(__o, Game):
            return self.game_id == __o.game_id
        return False

    def __hash__(self) -> int:
        """
        Hash the object
        """
        return hash(self.game_id)

    def __repr__(self) -> str:
        """
        Return the string representation of the object
        """
        return f"Game({self.game_id}, {self.name})"

    @classmethod
    def verify_fields(cls, data: dict) -> bool:
        """
        Check if the fields of the passed data are valid

        :param data: dict
        :return: bool
        """

        # Check if the fields are valid
        required_fields = [
            "game_id",
            "name",
            "added_at",
            "developer",
            "downloads",
            "pricing",
            "images",
            "details",
            "reviews",
            "tags",
        ]

        for field in required_fields:
            if field not in data:
                raise MissingRequiredField(f"Missing required field: {field}")

        # Check if the fields are correct
        for field, value in data.items():
            if field in cls.__annotations__:
                if not isinstance(value, cls.__annotations__[field]):
                    raise TypeError(f"Invalid type for field {field}")

        # Check if there are additional fields
        for field in data:
            if field not in cls.__annotations__:
                raise UnexpectedFieldError(f"Unexpected field: {field}")


class GameCollectionQuery:
    """
    Class responsible for querying the game collection
    """

    @staticmethod
    def get_product_by_game_id(game_id: str) -> Union[Game, None]:
        """
        Get a game by game_id

        :param game_id: str
        :return: Game
        """

        collection = mongo.cx["Catalog"]["games"]

        data = collection.find_one({"game_id": game_id})

        return Game(**data) if data else None

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

    @staticmethod
    def get_products_by_filters(
        start_at: int = None,
        limit: int = None,
        tag: str = None,
        developer: str = None,
        # Tuple unpacking
        **kwargs,
    ) -> list:

        """
        Returns all games from the product collection that contain the passed tag
        The method supports passing parameters explicitly or via kwargs
        If both are passed, only kwargs will be considered.
        This implies that explicitly passed parameters will take precedence over kwargs
        Also, different filters can be passed if using by kwargs, although the result is unexpected
        """

        if kwargs:
            filters = kwargs
        else:
            filters = {
                "tags": {"$in": [tag]},
                "developer": developer,
                "game_id": game_id,
            }

        collection = mongo.cx["Catalog"]["games"]
        result = collection.find(filters).skip(start_at).limit(limit)
        result = [Game(**game) for game in result]
        return result

    @staticmethod
    def full_text_search(query_text: str) -> list:
        """
        Returns all games from the product collection that contain the passed search string
        """

        collection = mongo.cx["Catalog"]["games"]
        search_pipeline = GameCollectionQuery().full_text_search_pipeline(query_text)
        result = collection.aggregate(search_pipeline)
        result = [Game(**game) for game in result]
        return result

    @staticmethod
    def generate_search_pipeline(query_text: str) -> list:
        """
        Generate the search pipeline
        """
        search_index = "default"

        pipeline = [
            {
                "$search": {
                    "index": search_index,
                    "text": {"query": query_text, "path": {"wildcard": "*"}},
                }
            }
        ]

        return pipeline

    @staticmethod
    def edit_product_by_gameId(query_id, **kwargs) -> bool:
        """
        Edit a game by game_id

        :param query_id: str
        :param kwargs: dict
        :return: bool
        """

        collection = mongo.cx["Catalog"]["games"]
        result = collection.update_one({"game_id": query_id}, {"$set": kwargs})
        return bool(result.modified_count)

    @staticmethod
    def delete_product_by_gameId(query_id) -> bool:
        """
        Delete a game by game_id

        :param query_id: str
        :return: bool
        """

        collection = mongo.cx["Catalog"]["games"]
        result = collection.delete_one({"game_id": query_id})
        return bool(result.deleted_count)

    @staticmethod
    def create_product(product: Game) -> bool:
        """
        Create a game into the game collection

        As the parameter is a Game object, we assume it is already validated


        :param product: Game
        :return: bool
        """

        # Verify if Game object is type Game
        if not isinstance(product, Game):
            return False

        game_dict = product.to_dict()

        # Delete the field _id if exists. Mongo creates automatically
        game_dict.pop("_id", None)

        # Add to db

        collection = mongo.cx["Catalog"]["games"]
        result = collection.insert_one(game_dict)
        return bool(result.inserted_id)


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
