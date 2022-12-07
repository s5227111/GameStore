from flask import Blueprint, render_template, url_for, redirect, request

from flask_login import current_user

import requests
from datetime import datetime

catalog = Blueprint(
    "catalog",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/catalog",
)

from api_catalog.models import Game


def configure(app):
    app.register_blueprint(catalog)


@catalog.route("/")
def home():

    user_games_ids = []
    user_games = []
    games_count = 0

    # Get all games
    home_games = requests.get(
        url_for("api_catalog.get_all_games", _external=True),
        params={"start_at": 0, "limit": 8},
        timeout=30,
    ).json()["data"]

    # If user is authenticated, get the games from my_games
    if current_user.is_authenticated:
        # As the table contains only indexes it is necessary to make a request on MongoDB
        user_games_ids = [game.game_id for game in current_user.my_games]

        # Search on the API the games that are on the list
        for game_id in user_games_ids:
            game = requests.get(
                url_for("api_catalog.get_all_games", _external=True),
                params={"game_id": game_id},
                timeout=30,
            ).json()["data"]
            user_games.append(game[0])

        games_count = len(user_games)

        # Change added_at to a more legible date
        for game in current_user.my_games:
            game.added_at = datetime.strftime(game.added_at, "%d/%m/%Y")

    return render_template(
        "catalog/index.html",
        home_games=home_games,
        user_games=user_games,
        games_count=games_count,
    )


@catalog.route("/details")
def details():
    game_id = request.args.get("game_id", None)
    game_id = int(game_id) if game_id else None
    is_in_my_games = False
    user_games_ids = []

    game_dict = requests.get(
        url_for("api_catalog.get_all_games", game_id=game_id, _external=True),
        params={"game_id": game_id},
        timeout=30,
    ).json()["data"]

    game_dict = game_dict[0] if game_dict else None

    if not game_dict:
        return redirect(url_for("catalog.home"))

    if current_user.is_authenticated:
        user_games_ids = [game.game_id for game in current_user.my_games]

    if game_id in user_games_ids:
        is_in_my_games = True

    # Related games
    game_tags = game_dict["tags"]
    related_games = []

    for tag in game_tags:

        related_games += requests.get(
            url_for("api_catalog.get_all_games", _external=True),
            params={"tags": tag},
            timeout=30,
        ).json()["data"]

        # As can have repetitions, get more than 8 games
        if len(related_games) >= 50:
            break

    # Remove games that user already has
    related_games = [
        Game(**game) for game in related_games if game["game_id"] not in user_games_ids
    ]

    # Remove repetitions
    related_games = set(related_games)

    # Get only 8 games
    related_games = list(related_games)[:8]

    return render_template(
        "catalog/details.html",
        game_dict=game_dict,
        related_games=related_games,
        is_in_my_games=is_in_my_games,
    )


@catalog.route("/browse")
def browse():
    return "Browse"


@catalog.route("/streams")
def streams():
    return "Streams"


@catalog.route("/profile")
def profile():
    return "Profile"