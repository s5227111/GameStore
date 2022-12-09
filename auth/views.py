# Flask packages and plugins
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
from .models import UserQuery, PersonalData, Contact, Address, PasswordReset

from flask_login import login_user, logout_user, login_required, current_user

# Serializers
from .serealizer import UserSchema
from marshmallow import ValidationError


# Views stores all end points (urls), ROTAS do meu projeto
# Blueprint: aplicacoes (funcionalidades dentro de um projeto) reutilizaveis
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
            username_email = request.form["username"]
            password = request.form["password"]
            # Try to find the user by email
            user = UserQuery.get_user_by_username_or_email(username_email)

            if user:
                # Berify if password is correct
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
    return render_template("auth/register.html")


@auth_bp.route("/validate-email", methods=["POST", "GET"])
def validate_email():

    # Verify if email is already exists
    email_exists = False

    if request.method == "POST":

        try:
            email = request.form["email"]

            # Verify if email is already exists
            user = UserQuery.get_user_by_email(email)

            if user:
                email_exists = True

                return (
                    render_template(
                        "auth/validate_email.html", email_exists=email_exists
                    ),
                    400,
                )

            # TODO SEND CONFIRMATION EMAIL
            session["email"] = email
            session["on_register"] = True

            return redirect(url_for("auth.validate_username"))

        except KeyError:

            return redirect("auth.register"), 400

    return render_template("auth/validate_email.html"), 200


@auth_bp.route("/validate-username", methods=["POST", "GET"])
def validate_username():

    username_exists = False

    if request.method == "POST":
        try:
            username = request.form["username"]

            # Verify if username is already exists
            user = UserQuery.get_user_by_username(username)

            if user:
                username_exists = True
                return render_template(
                    "auth/validate_username.html", username_exists=username_exists
                )

            # Verify if session has email and if user has validated email
            if session.get("email") and session.get("on_register"):
                session["username"] = username
                return redirect(url_for("auth.validate_password"))

        # Verify if username is already exists
        except KeyError():
            return render_template("auth.register")

    if session.get("email") and session.get("on_register"):
        return render_template("auth/validate_username.html")

    return redirect(url_for("auth.register"))


@auth_bp.route("/validate-password", methods=["POST", "GET"])
def validate_password():

    if request.method == "POST":
        try:
            password = request.form["password"]

            # Verify if session has email and if user has validated email

            password = request.form["password"]
            email = session["email"]
            username = session["username"]
            _ = session.pop("on_register")

            # Create user
            us = UserSchema()

            try:
                user = us.load(
                    {"username": username, "email": email, "password": password}
                )

                user_personal_data = PersonalData()
                user_contact = Contact()
                user_address = Address()
                user_password_reset = PasswordReset()

                user.personal_data = user_personal_data  # 1:1
                user.contact = user_contact  # 1:1
                user.address = user_address  # 1:1
                user.password_reset = user_password_reset  # 1:1

                current_app.db.session.add_all(
                    [
                        user,
                        user_personal_data,
                        user_contact,
                        user_address,
                        user_password_reset,
                    ]
                )

                current_app.db.session.commit()
                session.clear()
                return redirect(url_for("auth.login"))

            except ValidationError:
                return abort(404), 400

            return redirect(url_for("auth.confirmation"))

        except KeyError:
            return redirect("auth.register")

    if session.get("email") and session.get("username") and session.get("on_register"):
        return render_template("auth/validate_password.html")

    return redirect(url_for("auth.register"))


@auth_bp.route("/forgot-password", methods=["POST", "GET"])
def forgot_password():

    if request.method == "POST":
        try:
            email = request.form["email"]
            new_password = request.form["password"]

            # Verify if email is registered on the db
            user = UserQuery.get_user_by_email(email)

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

                current_app.db.session.commit()
                return redirect(url_for("auth.login"))

        # EMAIL NULL
        except KeyError:
            return abort(400)

    return render_template("auth/forgot_password.html")


@auth_bp.route("/profile", methods=["GET"])
@login_required
def profile():
    # IMPLEMENT USER PROFILE PAGE
    return render_template("auth/profile.html")


@auth_bp.route("/edit-profile", methods=["POST", "GET"])
@login_required
def edit_profile():
    # IMPLEMENT USER PROFILE PAGE

    current_user_data = UserQuery.get_user_by_id(current_user.id).to_dict()

    msgs = []

    if request.method == "POST":
        # UPDATE USER DATA
        data = request.form.to_dict()
        data = {k: v for k, v in data.items() if v}  # Remove empty values

        login_fields = ["username", "email", "password"]
        personal_data_fields = ["first_name", "last_name", "dob"]
        contact_fields = ["phone", "mobile"]
        address_fields = ["address_1", "address_2", "town_city", "county", "postcode"]

        # Verify if the user is trying to update login data
        if any(field in data for field in login_fields):

            try:
                UserQuery.update_login_data(current_user.id, data)
                msgs.append("Login data updated successfully")
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
        "auth/edit_profile.html", current_user_data=current_user_data, msgs=msgs
    )


# Error handlers
@auth_bp.errorhandler(404)
def page_not_found(e):
    return render_template("auth/404.html"), 404
