from cloud_tools import get_games_collection, generate_json_response

import functions_framework

from flask import request


@functions_framework.http
def get_game_by_id(request):

    """
    Get a game by id. The game id is passed as a query parameter.
    Different from the ``get_game_by_category`` function, this function will return only one game.
    So, if the game is not found, the function will return a 404 status code.
    """

    # Get the game id from the url
    game_id = request.args.get("game_id", None)

    # Try to convert the game id to an integer
    try:
        game_id = int(game_id)

    except ValueError:
        return generate_json_response(
            status_code=400,
            message="Invalid game_id",
            request_params=request.args,
            data=[],
        )

    if not game_id:
        return generate_json_response(
            status_code=400,
            message="game_id is required",
            request_params=request.args,
            data=[],
        )

    # Connect to the database
    collection = get_games_collection()

    # Search for the game
    game = collection.find_one({"game_id": game_id})

    if not game:
        return generate_json_response(
            status_code=404,
            message="No game found",
            request_params=request.args,
            data=[],
        )

    # Generate a json response with the game
    return generate_json_response(
        status_code=200,
        message="Success",
        request_params=request.args,
        data=[game],
    )
