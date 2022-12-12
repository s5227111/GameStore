import functions_framework
from pymongo import MongoClient
from bson.json_util import dumps
import json

from cloud_tools import generate_json_response, get_games_collection


@functions_framework.http
def full_text_search(request) -> list:

    """
    Returns all games from the product collection that contain the passed search string
    This function use mongodb full text search engine. To control the search engine,
    we need to create a index. For our case, we will create a index with the name "default"
    and set the index to match all the fields in the document, and same weight for all the fields.
    also, ``generate_search_pipeline`` function will generate the search pipeline to be used in the search query.
    """

    # Get the query text from the url
    query_text = request.args.get("query_text", None)
    sort_by = request.args.get("sort_by", None)
    sort_type = request.args.get("sort_type", 1)
    start_at = request.args.get("start_at", 0)
    limit = request.args.get("limit", 10)

    try:
        start_at = int(start_at)
    except ValueError:
        start_at = 0

    try:
        limit = int(limit)
    except ValueError:
        limit = 10

    try:
        sort_type = int(sort_type)

    except ValueError:
        sort_type = 1

    if not query_text:

        return generate_json_response(
            status_code=404,
            message="Query text cant be empty",
            request_params={"query_text": query_text},
            data=[],
        )  # type: ignore

    collection = get_games_collection()

    search_pipeline = generate_search_pipeline(query_text, sort_by, sort_type, start_at, limit)  # type: ignore because im converting sort_type to int # noqa: E501
    result = collection.aggregate(search_pipeline)
    result = [json.loads(dumps(r)) for r in result]

    # Return the result
    return generate_json_response(
        status_code=200,
        message="Success",
        request_params={"query_text": query_text},
        data=result,
    )  # type: ignore # noqa: E501


def generate_search_pipeline(query_text: str, sort_by: str = None, sort_type: int = 1, start_at: int = 0, limit: int = 10) -> list:  # type: ignore # noqa: E501

    """
    Generate the search pipeline to be used in the search query.
    """

    search_index = "default"

    # If sort_by is None, we will sort by score
    if not sort_by:
        sort_by = {"score": {"$meta": "textScore"}}  # type: ignore # noqa: E501

    else:
        sort_by = {sort_by: sort_type}  # type: ignore # noqa: E501

    pipeline = [
        {
            "$search": {
                "index": search_index,
                "text": {"query": query_text, "path": {"wildcard": "*"}},
            }
        },
        {"$sort": sort_by},
        {"$skip": start_at},
        {"$limit": limit},
    ]

    return pipeline
