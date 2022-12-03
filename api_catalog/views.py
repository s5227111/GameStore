from flask import Blueprint, request, jsonify

from typing import Union

from .models import GameCollectionQuery

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

    request_params = {"start_at": start_at, "limit": limit}

    # If the limit is greater than 100, the API will return only 100 results
    # If start_at is negative,
    limit = limit if limit <= 100 and limit > 0 else 100
    start_at = start_at if start_at >= 0 else 0

    filters = {"tag": tag}

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
    response = generate_json_response(
        status_code=404,
        data=[],
        request_params={"query_text": query_text},
        results=0,
        message="Not Found any game",
    )


@api_catalog.route("/", methods=["GET"])
def hello_world():
    return "Hello World"
