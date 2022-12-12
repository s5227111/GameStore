from flask import Request, jsonify, Response
from typing import Union


def generate_json_response(
    status_code: int,
    message: str,
    request_params: dict,
    data: Union[dict, list],
    **others
) -> Response:

    """
    This function returns a json response with the data passed as parameter.
    This function is used to generate a json response for all the endpoints in cloud functions.
    With this function, we can avoid to repeat the same code and keep a standard response for this application


    params:
        status_code: Status code to be returned in the response
        message: Message to be returned in the response
        request_params: Request parameters to be returned in the response
        data: Data to be returned in the response
        others: Other parameters to be returned in the response

    returns:
        Tuple with the json response and the status code, this tuple is used by the flask framework to return the response
    """

    response = {
        "status_code": status_code,
        "message": message,
        "request_params": request_params,
        "data": data,
    }

    for key, value in others.items():
        response[key] = value

    return jsonify(response)
