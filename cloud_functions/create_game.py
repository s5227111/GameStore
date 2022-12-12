import functions_framework

from pymongo import MongoClient
from bson.json_util import dumps

import json
import jwt

from game import Game
from cloud_tools import (
    get_games_collection,
    generate_json_response,
    verify_jwt_access_token,
)

from flask import request


@functions_framework.http
def create_game(request):

    # Verify the jwt token
    try:
        payload = verify_jwt_access_token(request)

    except Exception as e:  # type: ignore we can use except because we are already handling the error in the function
        return generate_json_response(
            status_code=401,
            message="Invalid token",
            data=e.args,  # type: ignore there is no data to return
            request_params=request.args.to_dict(),
        )

    # We just accept data from form! If the data is in json, we will return a error
    data = (
        request.get_json()
    )  # TODO: Estou recebendo um json para testar, mas o ideal é receber um form

    # Try to instantiate a game object. If the data is invalid, the function will return a error and
    # the game object will not be created and a error response will be returned
    try:
        game = Game(**data)  # type: ignore because this class is a dataclass, so we dont need to pass the parameters by name

        # If the game is valid, we need to connect to the database and insert the game
        collection = get_games_collection()

        # Generate a new id for the game
        game_id = collection.count_documents({}) + 1
        game["game_id"] = game_id

        # Insert the game in the database
        collection.insert_one(game.__dict__)

        # Return a success response
        return generate_json_response(
            status_code=200,
            message="Game created",
            data=game["game_id"],
            request_params=data,
        )

    except (ValueError, TypeError) as e:
        return generate_json_response(
            status_code=400,
            message="Invalid data",
            data=e.args,  # type: ignore there is no data to return
            request_params=data,
        )
