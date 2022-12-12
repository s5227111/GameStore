# Content:
# This file contains useful functions to be used in the cloud functions
# Some of the functions are used in more than one cloud function, so, we put them here to avoid code repetition
# In the future, we can add more functions here
# Also, its a good idea to put the functions here because we can use them in the web app
# ? Maybe we can create a way to sync the functions here with the web app, or maybe we can create a package to be used in both without
# ? add this file in every cloud function
# !Important: This file is not a cloud function, so, we need to be careful with the imports


"""
Dependencies: (need to be placed in the requirements.txt file)
 - flask
 - pymongo
 - pyjwt
 - cryptography
"""

from flask import Request, jsonify, Response
from typing import Union

from pymongo import MongoClient
import jwt
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError


def generate_json_response(
    status_code: int,
    message: str,
    request_params: dict,
    data: Union[dict, list],
    **others,
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

    Cloud functions that use this function:
        - create_game
        - edit_game_by_id
        - delete_game_by_id
        - get_game_by_category
        - get_game_by_full_text_search
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


def get_games_collection():
    """
    This function returns the games collection
    # * Legacy warning: If we change the database, we need to change this function
    """

    db_uri = "mongodb+srv://root:1234@cluster0.gg84ero.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(db_uri)
    db = client["Catalog"]
    collection = db.games

    return collection


def get_cloud_function_url(function_name: str) -> str:
    """
    This function returns the url of the cloud function passed as parameter
    # * Legacy warning: This url is hardcoded, so, if we change the cloud function name or project infos, we need to change this function
    # ? Maybe we can get this url from the environment variables
    """

    return (
        f"https://us-central1-teste-371002.cloudfunctions.net/{function_name}"
    )


def verify_jwt_access_token(request: Request):

    """
    This function verifies the jwt access token passed by the request header
    If the token is valid, the function returns the decoded token

    params:
        request: HTTP request object.

    returns:
        Decoded token if the token is valid

    raises:
        401: If the token is not valid
        400: If the token is not passed in the request header

    # * Legacy warning: ``public_key.pem`` is hardcoded, so, if we change the key, we need to change this function
    """

    with open("public_key.pem", "r", encoding="utf-8") as arch:
        public_key = (
            arch.read()
        )  # Is a good practice to read the key from a file, so, we can change the key without change the code
        # Also, use a file is more secure than use a variable

    token = request.headers.get("Authorization", None)

    # If token is None, the token was not passed in the request header. So, return a error value error
    if not token:
        raise ValueError("Token not passed in the request header")

    # If the token is not None, we need to verify the token
    # If the token is valid, we return the decoded token
    # If the token is not valid, we return a  InvalidSignatureError or ExpiredSignatureError
    try:
        decoded_token = jwt.decode(token, public_key, algorithms=["RS256"])

        # If the token is valid, we return the decoded token
        return decoded_token

    except (InvalidSignatureError, ExpiredSignatureError) as e:
        raise e


def generate_jwt_access_token(payload: dict) -> str:
    """
    This function generates a jwt access token with the payload passed as parameter

    # * Legacy warning: ``private_key.pem`` is hardcoded, so, if we change the key, we need to change this function
    """
    # ! Important: For some reason, the private key is not working with the ``open`` function, so we need to use full path to the file
    # ! but it works fine in google cloud functions
    private_key = open(
        r"C:\Users\jedma\Desktop\projects\clone\GameStore\cloud_functions\private_key.pem",
        encoding="utf-8",
    ).read()
    # Is a good practice to read the key from a file, so, we can change the key without change the code
    # Also, use a file is more secure than use a variable

    token = jwt.encode(payload, private_key, algorithm="RS256")

    return token


def generate_jwt_header(token: str) -> dict:
    """
    This function generates a jwt header with the token passed as parameter
    """

    return {"alg": "RS256", "typ": "JWT", "Authorization": token}
