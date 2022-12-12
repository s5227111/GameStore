import functions_framework
from pymongo import MongoClient
from bson.json_util import dumps
from json_response_generator import generate_json_response
import json
import jwt


@functions_framework.http
def get_games_by_tags(request):
    """
    This function returns a game by category. It will be called when
    the endpoint is triggered by a HTTP request.
    This endpoint dont need any authorization
    The url is generated by Google Cloud Functions
    api_url = https://us-central1-teste-371002.cloudfunctions.net/get_games_by_tags?

    This endpoint need a tag as parameter, this parameter is passed by the url.

    params:
        request: HTTP request object.
        tag: Category of the game to be returned (passed by the url)
        sort_by: Sort the games by this parameter (passed by the url)
    returns:
        Json response with the game data

    Notes:
        - if the tag is not passed by the url, the function will return all the games, limited by the limit parameter
        - if the sort_by parameter is not passed by the url, the function will return the games sorted by the name
        - if the sort_by parameter is not valid, the function will ignore and return all the games without sorting
        - Multiples tags search are not supported.
        - If you want to sort by a filed in a subdocument, you can use dotted reference, like ``reviews.starts``
    """

    # Verify request jwt signature 
    # Get the token from the header
    token = request.headers.get("Authorization", None)
    
 
    # Get the tag from the url
    tag = request.args.get("tag", None)
    sort_by = request.args.get("sort_by", "name")

    # Get the limit and start_at from the url
    limit = request.args.get("limit", 100)
    start_at = request.args.get("start_at", 0)

    # Set the limit and start_at to int
    limit = int(limit)
    start_at = int(start_at)

    # Get the request params
    request_params = request.args

    # Connect to the database
    client = MongoClient(
        "mongodb+srv://root:1234@cluster0.gg84ero.mongodb.net/?retryWrites=true&w=majority"
    )
    db = client["Catalog"]

    # Get the collection
    collection = db["games"]

    # Search for the games

    if tag:
        query_filter = {"tags": {"$in": [tag]}}
    else:
        query_filter = {}

    games = (
        collection.find(query_filter).sort(sort_by).skip(start_at).limit(limit)
    )

    # Convert the games to json
    games_list = [json.loads(dumps(r)) for r in games]

    if not games_list:
        # Generate a json response with the error message
        return generate_json_response(
            status_code=404,
            message="No games found",
            request_params=request_params,
            data=games_list,
        )

    # Generate a json response with the games
    return generate_json_response(
        status_code=200,
        message="Success",
        request_params=request_params,
        data=games_list,
    )
