from flask import Blueprint, render_template, url_for

from flask_login import current_user

import requests

catalog = Blueprint(
    "catalog",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/catalog",
)


def configure(app):
    app.register_blueprint(catalog)


@catalog.route("/")
def home():

    # Get all games
    home_games = requests.get(
        url_for("api_catalog.get_all_games", _external=True),
        params={"start_at": 0, "limit": 8},
        timeout=30,
    ).json()["data"]

    return render_template("catalog/index.html", home_games=home_games)


@catalog.route("/details/<int:game_id>")
def details(game_id):
    return game_id


@catalog.route("/browse")
def browse():
    return "Browse"


@catalog.route("/streams")
def streams():
    return "Streams"


@catalog.route("/profile")
def profile():
    return "Profile"
