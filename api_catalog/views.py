from flask import Blueprint, request, jsonify

from typing import Union

from .models import GameCollectionQuery, Game

from .api_errors import MissingRequiredField, UnexpectedFieldError, DuplicateGameIdError

api_catalog = Blueprint("api_catalog", __name__, url_prefix="/apis/catalogApi")


def configure(app):
    app.register_blueprint(api_catalog)


def generate_json_response(
    status_code: int,
    data: Union[list, dict],
    request_params: dict,
    results: int,
    message: str = None,
) -> dict:
    """
    Gera um json de resposta para as buscas da api.
    Isso nos garante uma padronização de resposta para as buscas

    :param status_code: int - Código de status da resposta
    :param data: list - Lista de dados retornados
    :param resquest_params: dict - Dicionário com os parâmetros da requisição
    :param results: int - Número de resultados retornados
    :param message: str - Mensagem de erro, evite deixar nulo
    :return: dict

    """
    response = {
        "status_code": status_code,
        "request_params": request_params,
        "data": data,
        "results": results,
        "message": message,
    }

    return response


# GET GAMES
@api_catalog.route("/getAllGames/", methods=["GET"])
def get_all_games():
    """
    [General]
    Get all games from the game collection limited to 100 results/requisition
    This search does not use endpoint /searchGames/ TODO

    If the pagination param is not passed, the API will return the first 100 results
    If the params cannot be converted to int, the API will return the first 100 results

    Example of use:
    /apis/catalogApi/getAllGames/?start_at=0&limit=100 - Returns the first 100 results
    /apis/catalogApi/getAllGames/?start_at=100&limit=100 - Returns the second 100 results

    :param: start_at: int - number of products (json's documents) to skip
    :param: limit: int - number of products (json's documents) to return
    :return: json

    [Refining the search]
    """

    try:
        start_at = int(request.args.get("start_at", 0))
        limit = int(request.args.get("limit", 100))
    except ValueError:

        start_at = 0
        limit = 100

    # Filtering search params
    tag = request.args.get("tag", None)
    developer = request.args.get("developer", None)

    request_params = {"start_at": start_at, "limit": limit}

    # If the limit is greater than 100, the API will return only 100 results
    # If start_at is negative,
    limit = limit if limit <= 100 and limit > 0 else 100
    start_at = start_at if start_at >= 0 else 0

    filters = {"tag": tag, "developer": developer}

    if any(filters.values()):
        games = GameCollectionQuery.get_products_by_filters(start_at, limit, **filters)
    else:
        games = GameCollectionQuery.get_all_products(start_at, limit)

    # Generate the response
    if games:
        response = generate_json_response(
            status_code=200,
            data=games,
            request_params=request_params,
            results=len(games),
            message="Success",
        )

        return jsonify(response), 200

    # Caso a busca não encontre resultados, nosso padrão é retornar um json de erro
    response = generate_json_response(
        status_code=404,
        data=[],
        request_params=request_params,
        results=0,
        message="Not Found",
    )
    return jsonify(response), 404


# SEARCH GAMES
@api_catalog.route("/searchGames/", methods=["GET"])
def search_games():
    """
    Uses the engine of fulltext to make searches by text
    The fields are controlled internally by the method "GameCollectionQuery.generate_search_pipeline"
    """

    query_text = request.args.get("query_text", None)
    games = GameCollectionQuery.search_products(query_text)

    if games:
        response = generate_json_response(
            status_code=200,
            data=games,
            request_params={"query_text": query_text},
            results=len(games),
            message="Success",
        )

        return jsonify(response), 200

    # If don't find results, json error is returned
    return (
        jsonify(
            generate_json_response(
                status_code=404,
                data=[],
                request_params={"query_text": query_text},
                results=0,
                message="Not Found any game",
            )
        ),
        404,
    )


@api_catalog.route("/editProduct", methods=["PUT"])
def edit_product():
    """
    [General]
    Edit a product by id

    [Params]
    game_id: str - id of the game to be edited
    data_to_edit: dict - data to be edited, should be passed as params of the request

    [Response json]
    Some examples of response json:
    "Field not found in the games collection"
    "Product edited with success"
    "Not Found any game"
    """

    # import ipdb

    # ipdb.set_trace()

    # Request params
    game_id = int(request.args.get("game_id", None))
    data_to_edit = request.get_json()

    # Store request params
    request_params = request.args.to_dict()
    request_params["data_to_edit"] = data_to_edit
    msg = ""

    # Required params
    if game_id and data_to_edit:
        # check if product exists

        product = GameCollectionQuery.get_product_by_game_id(game_id)

        # Check if field is on the schema
        for key in data_to_edit.keys():
            if key not in Game.__annotations__:
                product = None
                msg = "Field not found in the games collection"
                break

        if product:

            # Edit product
            GameCollectionQuery.edit_product_by_gameId(game_id, **data_to_edit)
            msg = "Product edited with success"

            return (
                jsonify(
                    generate_json_response(
                        status_code=200,
                        data=None,
                        request_params=request_params,
                        results=1,
                        message=msg,
                    )
                ),
                200,
            )

        msg = "Product not found" if not msg else msg

        # If don't find results, json error is returned
        # If the product is not found, the API will return a json error
        # This is necessary response json will be generated corrctly

        msg = "Product not found" if not msg else msg
        return (
            jsonify(
                generate_json_response(
                    status_code=400,
                    data=None,
                    request_params=request_params,
                    results=None,
                    message=msg,
                )
            ),
            400,
        )


# DELETE by Id
@api_catalog.route("/deleteProduct", methods=["DELETE"])
def delete_product():
    """
    [General]
    Delete a product by id

    [Params]
    game_id: str - id of the game to be deleted
    """

    # Request params
    game_id = int(request.args.get("game_id", None))

    # Store request params
    request_params = request.args.to_dict()
    msg = ""

    # Required params
    if game_id:
        # check if product exists

        product = GameCollectionQuery.get_product_by_game_id(game_id)

        if product:

            # Delete product
            GameCollectionQuery.delete_product_by_gameId(game_id)
            msg = "Product deleted with success"

            return (
                jsonify(
                    generate_json_response(
                        status_code=200,
                        data=None,
                        request_params=request_params,
                        results=1,
                        message=msg,
                    )
                ),
                200,
            )

        msg = "Product not found" if not msg else msg

        # If don't find results, json error is returned
        # If the product is not found, the API will return a json error
        # This is necessary response json will be generated corrctly

        msg = "Product not found" if not msg else msg
        return (
            jsonify(
                generate_json_response(
                    status_code=400,
                    data=None,
                    request_params=request_params,
                    results=None,
                    message=msg,
                )
            ),
            400,
        )


# Create a new product
@api_catalog.route("/createProduct", methods=["POST"])
def createProduct():
    """
    [General]
    Create a new product

    [Params]
    data_to_create: dict - data to be created, should be passed as params of the request

    [Response json]
    Some examples of response json:
    "Field not found in the games collection"
    "Product created with success"
    "Not Found any game"
    """

    # import ipdb

    # ipdb.set_trace()

    # Request params
    data_to_create = request.get_json()

    # Store request params
    request_params = request.args.to_dict()
    request_params["data_to_create"] = data_to_create

    msg = ""

    # Instantiate Obj Game with data passed on the request

    try:
        # Validate data, Exception if invalid
        # Missing fields
        _ = Game.verify_fields(data_to_create)
        product = Game(**data_to_create)

        # Verify if product already exists
        if GameCollectionQuery.get_product_by_game_id(product.game_id):
            msg = "Product already exists"
            raise DuplicateGameIdError(msg)

        # Create product, if don't exists
        GameCollectionQuery.create_product(product)
        msg = "Product created with success"

        return (
            jsonify(
                generate_json_response(
                    status_code=200,
                    data=[msg],
                    request_params=request_params,
                    results=1,
                    message=msg,
                )
            ),
            200,
        )

    except (UnexpectedFieldError, MissingRequiredField, DuplicateGameIdError) as e:
        msg = msg if msg else str(e)

        return (
            jsonify(
                generate_json_response(
                    status_code=400,
                    data=None,
                    request_params=request_params,
                    results=None,
                    message=msg,
                )
            ),
            400,
        )


@api_catalog.route("/", methods=["GET"])
def hello_world():
    return "Hello World"
