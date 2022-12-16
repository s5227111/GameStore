# Flask packages and plugins
# TABLE OF CONTENTS
# 1. Imports
# 2. Login Routes
# 3. Logout Route
# 4. Register Route
# 5. Forgot Password Route !TODO Currently, this application does not have a mail server
# 7. Verify Email Route !TODO Currently, this application does not have a mail server
# 8. Configure Blueprint


from flask import (
    Blueprint,
    render_template,
    url_for,
    request,
    abort,
    session,
    redirect,
    current_app,
)

# Models
from .models import (
    UserQuery,
    PersonalData,
    Contact,
    Address,
    User,
)

from flask_login import login_user, logout_user, login_required, current_user

# Serializers
from .serealizer import UserSchema
from marshmallow import ValidationError

import requests

from cloud_functions.cloud_tools import get_cloud_function_url

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/user",
)


def configure(app):
    app.register_blueprint(auth_bp)
    app.config["SECRET_KEY"] = "p'e5'7phBEdm3g]jHdtS"


# Login Routes
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        try:
            email = request.form["email"]
            password = request.form["password"]
            # Try to find the user by email
            user = User.query.filter_by(email=email).first()

            if user:
                # Verify if password is correct
                if user.check_password_hash(password):
                    # Login user
                    login_user(user)
                    return redirect(url_for("catalog.home"))

            # If do not find username or pwd
            wrong_credentials = True
            return render_template(
                "auth/login.html", wrong_credentials=wrong_credentials
            )

        # Username or pwd is NULL
        except KeyError:
            return abort(400)

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("catalog.home"))


@auth_bp.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "POST":
        try:

            email = request.form["email"]
            username = request.form["username"]
            password = request.form["password"]

            # Verify if email is already exists
            user = User.query.filter_by(email=email).first()
            if user:
                return render_template("auth/register.html", email_exists=True)

            # Verify if username is already exists
            user = User.query.filter_by(username=username).first()

            if user:
                return render_template("auth/register.html", username_exists=True)

            # Create user
            us = UserSchema()
            user = us.load(
                {
                    "email": email,
                    "username": username,
                    "password": password,
                }
            )
            # Add relationship with other tables
            user.personal_data = PersonalData()
            user.contact = Contact()
            user.address = Address()

            # Save user
            user.save()
            login_user(user)

            return redirect(url_for("catalog.home"))

        # For some reason, the user did not fill in the email field
        except KeyError:
            return redirect(url_for("auth.register"))

    return render_template("auth/register.html")


@auth_bp.route("/forgot-password", methods=["POST", "GET"])
def forgot_password():

    if request.method == "POST":
        try:
            email = request.form["email"]
            new_password = request.form["password"]

            # Verify if email is registered on the db
            user = User.query.filter_by(email=email).first()

            if user:
                # Send email to retrieve password

                # Assumes that all is validated to change password
                # TODO IMPLEMENT EMAIL SENDING WITH TOKEN TO RETRIEVE PASSWORD
                user.password = new_password
                user.hash_password()

                # Update PasswordReset table
                user.password_reset.token = (
                    None  # When implement email sending, remove this line
                )
                user.password_reset.is_used = (
                    True  # When implement email sending, remove this line
                )

                current_app.db.session.commit()  # type: ignore
                return redirect(url_for("auth.login"))

        # EMAIL NULL
        except KeyError:
            return abort(400)

    return render_template("auth/forgot_password.html")


@auth_bp.route("/profile", methods=["GET"])
@login_required
def profile():

    current_user_data = current_user.to_dict()
    current_user_games_ids = current_user_data["my_games"]

    # Get user games
    # Note: the user ``my_games`` is a list of games ids. To get the games data, we need to use ``catalog_api``
    # The games data is stored in the catalog database in mongoDB
    # Note: in future, functions GET type in ``catalog_api`` will be a cloud functions.
    # This functions will need to change the way to get the data

    # Get user games
    user_games = []

    # Get cloud function url
    get_game_by_id_url = get_cloud_function_url("get_game_by_id")

    for g in current_user_games_ids:

        game = requests.get(
            get_game_by_id_url,
            timeout=30,
            params={"game_id": g["game_id"]},
        ).json()["data"][0]

        user_games.append(game)

    # Get user cart
    # idem to user games
    user_cart = []

    for g in current_user_data["user_cart"]:
        game = requests.get(
            get_game_by_id_url,
            timeout=30,
            params={"game_id": g["game_id"]},
        ).json()["data"][0]

        user_cart.append(game)

    # Get user history
    # idem to user games and user
    user_history = []

    for g in current_user_data["products_history"]:
        game = requests.get(
            get_game_by_id_url,
            timeout=30,
            params={"game_id": g["game_id"]},
        ).json()["data"][0]

        user_history.append(game)

    return render_template(
        "auth/profile.html",
        user_cart=user_cart,
        user_games=user_games,
        user_history=user_history,
    )


@auth_bp.route("/edit-profile", methods=["POST", "GET"])
@login_required
def edit_profile():

    current_user_data = current_user.to_dict()

    msgs = []

    if request.method == "POST":
        # UPDATE USER DATA
        data = request.form.to_dict()
        data = {k: v for k, v in data.items() if v}  # Remove empty values

        login_fields = ["username", "email", "password"]
        personal_data_fields = ["first_name", "last_name", "dob"]
        contact_fields = ["phone", "mobile"]
        address_fields = [
            "address_1",
            "address_2",
            "town_city",
            "county",
            "postcode",
        ]

        # Verify if the user is trying to update login data
        if any(field in data for field in login_fields):

            try:
                UserQuery.update_login_data(current_user.id, data)
                msgs.append("Login data updated")
                return render_template(
                    "auth/edit_profile.html",
                    msgs=msgs,
                    current_user_data=current_user_data,
                )

            except ValidationError as err:
                msgs.append(err.messages)

            return render_template(
                template_name_or_list="auth/edit_profile.html",
                msgs=msgs,
                current_user_data=current_user_data,
            )

        # Verify if the user is trying to update personal data
        if any(field in data for field in personal_data_fields):

            try:
                UserQuery.update_personal_data(current_user.id, data)
                return redirect(url_for("auth.profile"))

            except ValidationError as err:
                msgs.append(err.messages)

            return render_template(
                template_name_or_list="auth/edit_profile.html",
                msgs=msgs,
                current_user_data=current_user_data,
            )

        # Verify if the user is trying to update contact data
        if any(field in data for field in contact_fields):

            try:
                UserQuery.update_contact_data(current_user.id, data)
                return redirect(url_for("auth.profile"))

            except ValidationError as err:
                msgs.append(err.messages)

            return render_template(
                template_name_or_list="auth/edit_profile.html",
                msgs=msgs,
                current_user_data=current_user_data,
            )

        # Verify if the user is trying to update address data
        if any(field in data for field in address_fields):

            try:
                UserQuery.update_address_data(current_user.id, data)
                return redirect(url_for("auth.profile"))

            except ValidationError as err:
                msgs.append(err.messages)

            return render_template(
                template_name_or_list="auth/edit_profile.html",
                msgs=msgs,
                current_user_data=current_user_data,
            )

    return render_template(
        "auth/edit_profile.html",
        current_user_data=current_user_data,
        msgs=msgs,
    )


# Error handlers
@auth_bp.errorhandler(404)
def page_not_found(e):
    return render_template("auth/404.html"), 404
