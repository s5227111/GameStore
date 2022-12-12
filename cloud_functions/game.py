# CONTENT:
# A single class that handles the game logic
# Its used to create a game object and guarantee an semi-established structure
# for the game data

from dataclasses import dataclass


@dataclass
class Game:

    """
    This class is used to represent a game in catalog
    With that, we can guarantee some semi-structure for our games in catalog.
    Note that this class is not used to validate the data, but to guarantee a semi-structure
    Also, this class is used to create a game object from a dict
    At the end, game_id and _id are not necessary because 1. we will generate a game_id and 2. mongo db will auto generate an __id

    !Important: If a filed not listed here is passed, an error will be raised. So, if you want to add a new field,
    ! you likely will can add it in some subfield, like details, reviews, etc.

    # TODO: A post-init method to add fields that are not listed here. For while, we will raise an error

    # ? Maybe we can use a dict to store the data, but I think that this is not a good idea because we will lose the type hinting
    # ? and we will need to check the type of the data in the post-init method

    # * Legacy code warning: This class was created to be used in the cloud functions, but it can be used in other places
    # * like the web app, so, we need to be careful with the imports * #
    """

    # _id  is not necessary because mongo db add it

    name: str
    added_at: str
    developer: str
    downloads: int
    pricing: float
    tags: list
    images: dict
    details: dict
    reviews: dict
    game_id: int = None  # type: ignore this field is not necessary because we will generate a game_id

    def __post_init__(self) -> None:
        self.__check_required_fields__()

    def __check_required_fields__(self):

        """
        Check if all required fields have the correct type
        """

        for field in Game.__annotations__:
            if not isinstance(
                getattr(self, field), Game.__annotations__[field]
            ) and getattr(self, field) is not None:
                raise ValueError(
                    f"Field {field} must be instance of {Game.__annotations__[field]}"
                )
        return True

    def __getitem__(self, item):

        return getattr(self, item)

    def __setitem__(self, key, item):
        setattr(self, key, item)
