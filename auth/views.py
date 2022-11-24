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


@auth_bp.route("/")
def home():
    return render_template("auth/home.html")


# Login Routes
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        try:
            username_email = request.form["username"]
            password = request.form["password"]
            # Try to find the user by email
            user = UserQuery.get_user_by_email(username_email)

            if user:
                # Berify if password is correct
                if user.check_password_hash(password):
                    # Login user
                    login_user(user)
                    return redirect(url_for("auth.home"))

            # If do not find username or pwd
            wrong_credentials = True
            return render_template(
                "auth/login.html", wrong_credentials=wrong_credentials
            )

        # Username or pwd is NULL
        except KeyError:
            return abort(400)

    return render_template("auth/login.html")


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
                return redirect(url_for("auth.home"))

            except ValidationError:
                return abort(404), 400

            return redirect(url_for("auth.confirmation"))

        except KeyError:
            return redirect("auth.register")

    if session.get("email") and session.get("username") and session.get("on_register"):
        return render_template("auth/validate_password.html")

    return redirect(url_for("auth.register"))


# Error handlers
@auth_bp.errorhandler(404)
def page_not_found(e):
    return render_template("auth/404.html"), 404
