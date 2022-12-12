from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    request,
    current_app,
)

from auth.models import Upvotes, userCart, myGames

from flask_login import current_user, login_required

from cloud_functions.cloud_tools import (
    get_cloud_function_url,
    generate_jwt_access_token,
    generate_jwt_header,
)

import requests
from datetime import datetime

catalog = Blueprint(
    "catalog",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/catalog",
)


def configure(app):
    app.register_blueprint(catalog)


@catalog.route("/")  # type: ignore # noqa
def home():

    user_games_ids = []
    user_games = []
    games_count = 0

    # Get the cloud functions urls
    get_games_by_tag_url = get_cloud_function_url("get_games_by_tags")
    get_games_by_id_url = get_cloud_function_url("get-game-by-id")

    # Get all games
    home_games = requests.get(
        get_games_by_tag_url,
        params={"start_at": 0, "limit": 8, "sort_by": "date_added"},
        timeout=30,
    ).json()["data"]

    # If user is authenticated, get the games from my_games
    if current_user.is_authenticated:
        # As the table contains only indexes it is necessary to make a request on MongoDB
        user_games_ids = [game.game_id for game in current_user.my_games]

        # Search on the API the games that are on the list
        for game_id in user_games_ids:
            game = requests.get(
                get_games_by_id_url,
                params={
                    "game_id": game_id,
                },
                timeout=30,
            ).json()["data"][
                0
            ]  # the API returns a list with one element, so we need to get the first element
            user_games.append(game)

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
    is_in_my_upvotes = False
    is_in_my_cart = False
    user_games_ids = []

    # Get the cloud functions urls
    get_games_by_id_url = get_cloud_function_url("get-game-by-id")
    get_games_by_tag_url = get_cloud_function_url("get_games_by_tags")

    game_dict = requests.get(
        get_games_by_id_url,
        params={"game_id": game_id},
        timeout=30,
    ).json()["data"]

    game_dict = game_dict[0] if game_dict else None

    if not game_dict:
        return redirect(url_for("catalog.home"))

    if current_user.is_authenticated:
        user_games_ids = [game.game_id for game in current_user.my_games]

        # Check if game is in my games
        if game_id in user_games_ids:
            is_in_my_games = True

        # Check if game is upvoted by user
        if game_id in [game.game_id for game in current_user.upvotes]:
            is_in_my_upvotes = True

        # Check if game is in user cart
        if game_id in [game.game_id for game in current_user.user_cart]:
            is_in_my_cart = True

        # If user is authenticated, save this game in his history
        current_user.add_products_history(game_id)

    # Related games
    game_tags = game_dict["tags"]
    related_games = []

    # Related games is games with the same tag
    related_games = requests.get(
        get_games_by_tag_url,
        params={
            "start_at": 0,
            "limit": 20,  # Get 20 games to remove repetitions
            "sort_by": "date_added",
            "tags": game_tags[0],
        },
        timeout=30,
    ).json()["data"]

    # Remove games that user already has
    related_games = [
        game for game in related_games if game["game_id"] not in user_games_ids
    ]

    # Get only 8 games
    related_games = list(related_games)[:8]

    return render_template(
        "catalog/details.html",
        game_dict=game_dict,
        related_games=related_games,
        is_in_my_games=is_in_my_games,
        is_in_my_upvotes=is_in_my_upvotes,
        is_in_my_cart=is_in_my_cart,
    )


@catalog.route("/browse")
def browse():

    most_upvoted_games = []
    # Get the cloud functions urls
    get_games_by_tag_url = get_cloud_function_url("get_games_by_tags")

    # Get the most upvoted games
    most_upvoted_games = requests.get(
        get_games_by_tag_url,
        params={"start_at": 0, "limit": 8, "sort_by": "reviews.stars"},
        timeout=30,
    ).json()["data"]

    most_downloaded_games = requests.get(
        get_games_by_tag_url,
        params={"start_at": 0, "limit": 3, "sort_by": "downloads"},
        timeout=30,
    ).json()["data"]

    most_upvoted_casual_games = requests.get(
        get_games_by_tag_url,
        params={
            "start_at": 0,
            "limit": 10,
            "sort_by": "reviews.stars",
            "tag": "Casual",
        },
        timeout=30,
    ).json()["data"]

    most_upvoted_offline_games = requests.get(
        get_games_by_tag_url,
        params={
            "start_at": 0,
            "limit": 10,
            "sort_by": "reviews.stars",
            "tag": "Offline",
        },
        timeout=30,
    ).json()["data"]

    most_upvoted_multiplayer_games = requests.get(
        get_games_by_tag_url,
        params={
            "start_at": 0,
            "limit": 10,
            "sort_by": "reviews.stars",
            "tag": "Multiplayer",
        },
        timeout=30,
    ).json()["data"]

    # Recent added games
    recent_added_games = requests.get(
        get_games_by_tag_url,
        params={"start_at": 0, "limit": 4, "sort_by": "added_at"},
        timeout=30,
    ).json()["data"]

    return render_template(
        "catalog/browse.html",
        most_upvoted_games=most_upvoted_games,
        most_downloaded_games=most_downloaded_games,
        most_upvoted_casual_games=most_upvoted_casual_games,
        most_upvoted_offline_games=most_upvoted_offline_games,
        most_upvoted_multiplayer_games=most_upvoted_multiplayer_games,
        recent_added_games=recent_added_games,
    )


@catalog.route("/upvote")
@login_required
def upvote():

    game_id = request.args.get("game_id", None)

    # Get the cloud functions urls
    get_game_by_id_url = get_cloud_function_url("get-game-by-id")
    edit_game_by_id_url = get_cloud_function_url("edit-product-by-id")
    # Get the game
    game = requests.get(
        get_game_by_id_url,
        params={"game_id": game_id},
        timeout=30,
    ).json()["data"][0]

    # If the game exists
    if game:
        data_to_edit = {"reviews.stars": game["reviews"]["stars"] + 1}

    # To update the game, it is necessary generate a jwt token
    payload = {
        "iss": "upvote",
        "sub": "upvote",
        "iat": datetime.now().timestamp(),
        "exp": datetime.now().timestamp() + 30,
        "data_to_edit": data_to_edit,  # type: ignore because data_to_edit is defined in the if, so its will never be unbounded
    }

    token = generate_jwt_access_token(payload)
    headers = generate_jwt_header(token)

    # Update the game
    _ = requests.put(
        edit_game_by_id_url,
        params={"game_id": game_id},
        timeout=30,
        headers=headers,
    ).json()

    # Add the user to the upvotes
    upvote_table = Upvotes(game_id=game_id, user_id=current_user.id)  # type: ignore because Upvotes is a model
    current_user.upvotes.append(upvote_table)
    current_user.save()

    return redirect(url_for("catalog.details", game_id=game_id))


@catalog.route("/downvote")
@login_required
def downvote():

    game_id = request.args.get("game_id", None)

    # Get the cloud functions urls
    get_game_by_id_url = get_cloud_function_url("get-game-by-id")
    edit_game_by_id_url = get_cloud_function_url("edit-product-by-id")

    # Get the upvote table
    upvote_table = Upvotes.query.filter_by(
        game_id=game_id, user_id=current_user.id
    ).first()

    if not upvote_table:
        return redirect(url_for("catalog.details", game_id=game_id))

    # Get the game
    game = requests.get(
        get_game_by_id_url,
        params={"game_id": game_id},
        timeout=30,
    ).json()["data"][0]

    # If the game exists
    if game:
        data_to_edit = {"reviews.stars": game["reviews"]["stars"] - 1}

    # To update the game, it is necessary generate a jwt token
    payload = {
        "iss": "downvote",
        "sub": "downvote",
        "iat": datetime.now().timestamp(),
        "exp": datetime.now().timestamp() + 30,
        "data_to_edit": data_to_edit,  # type: ignore because data_to_edit is defined in the if, so its will never be unbounded
    }

    token = generate_jwt_access_token(payload)
    headers = generate_jwt_header(token)

    # Update the game
    _ = requests.put(
        edit_game_by_id_url,
        params={"game_id": game_id},
        timeout=30,
        headers=headers,
    ).json()

    # delete the upvote
    current_user.upvotes.remove(upvote_table)
    current_app.db.session.delete(upvote_table)
    current_app.db.session.commit()

    return redirect(url_for("catalog.details", game_id=game_id))


@catalog.route("/add_to_my_cart")
@login_required
def add_to_my_cart():

    game_id = request.args.get("game_id", None)

    # Check if the game is already in the user's game
    if game_id in [game.game_id for game in current_user.my_games]:
        return redirect(url_for("catalog.details", game_id=game_id))

    # add the game to the user's cart
    cart_table = userCart(game_id=game_id, user_id=current_user.id)
    current_user.user_cart.append(cart_table)
    current_user.save()

    return redirect(url_for("catalog.details", game_id=game_id))


@catalog.route("/remove_from_my_cart")
@login_required
def remove_from_my_cart():

    game_id = request.args.get("game_id", None)
    landing_from = request.args.get(
        "landing_from", None
    )  # "details" or "profile"

    if landing_from == "details":
        redirect_url = "catalog.details"
    elif landing_from == "profile":
        redirect_url = "auth.profile"

    # Get the cart table
    cart_table = userCart.query.filter_by(
        game_id=game_id, user_id=current_user.id
    ).first()

    if not cart_table:
        return redirect(url_for(redirect_url, game_id=game_id))

    # delete the cart
    current_user.user_cart.remove(cart_table)
    current_app.db.session.delete(cart_table)
    current_app.db.session.commit()

    return redirect(url_for(redirect_url, game_id=game_id))


@catalog.route("/add_to_my_games")
@login_required
def add_to_my_games():

    game_id = request.args.get("game_id", None)

    # Check if the game is already in the user's game
    if game_id in [game.game_id for game in current_user.my_games]:
        return redirect(url_for("auth.profile", game_id=game_id))

    # Add the game to the user's games
    game_table = myGames(game_id=game_id, user_id=current_user.id)
    current_user.my_games.append(game_table)
    current_user.save()

    # Get the cart table and delete it
    cart_table = userCart.query.filter_by(
        game_id=game_id, user_id=current_user.id
    ).first()

    if cart_table:
        current_user.user_cart.remove(cart_table)
        current_app.db.session.delete(cart_table)
        current_app.db.session.commit()

    return redirect(url_for("auth.profile"))


@catalog.route("streams")
def streams():
    return "Streams"


@catalog.route("list_games", methods=["GET", "POST"])
def list_games():

    query = request.form.get(
        "searchKeyword", None
    )  # Default query is "games", so if the user don't type anything, it will return all games

    start_at = request.args.get("start_at", None)
    start_at = int(start_at) if start_at else 0

    # Maybe the query is in the url
    query = request.args.get("searchKeyword", "lorem") if not query else query

    # Get the sorting option, if the user don't select any option, it will be "relevance"
    sort_by = request.form.get(
        "sort_by", None
    )  # if the user don't select any option, it will be "relevance"
    sort_type = request.form.get(
        "sort_type", None
    )  # if the user don't select any option, it will be "desc"
    sort_type = int(sort_type) if sort_type else 1

    # Get the cloud functions urls
    get_games_url = get_cloud_function_url("get-product-by-full-textsearch")

    # Get the games
    games = requests.get(
        get_games_url,
        params={
            "query_text": query,
            "start_at": start_at,
            "limit": 10,
            "sort_by": sort_by,
            "sort_type": sort_type,
        },
        timeout=30,
    ).json()["data"]

    return render_template("catalog/list_games.html", games=games, query=query)
