# MANAGE APP.PY URLs
from flask import Blueprint, render_template, url_for, request, abort, session, redirect

from .models import UserQuery

# Views stores all end points (urls), ROTAS do meu projeto
# Blueprint: aplicacoes (funcionalidades dentro de um projeto) reutilizaveis
auth_bp = Blueprint(
    "auth", 
    __name__, 
    template_folder="templates", 
    static_folder="static",
    url_prefix="/user")

def configure(app):
    app.register_blueprint(auth_bp)
    app.config['SECRET_KEY'] = "p'e5'7phBEdm3g]jHdtS"

@auth_bp.route("/")
def home():
    return render_template("auth/home.html")

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

                # Json de retorno
                return_json = {
                    "error": "Email already exists",
                    "email_exists": email_exists,
                    "status_code": 400,
                }

                return render_template(
                    "auth/validate_email.html", 
                    email_exists=email_exists
                ), return_json, 400

            session["email"] = email
            session["on_register"] = True
            
            return_json = {
                    "error": "Email validated",
                    "email_exists": email_exists,
                    "status_code": 200,
            }

            return redirect(
                url_for("auth.validate-username")), 200, return_json

        except KeyError:

            return_json = {
                "error": "Email not found",
                "email_exists": email_exists,
                "status_code": 400,
            }
            return redirect("auth.register"), 400, return_json

    return render_template("auth/validate_email.html"), 200, return_json

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
                    "auth/validate_username.html", 
                    username_exists=username_exists
                    )
            
            # Verify if session has email and if user has validated email
            if session.get("email") and session.get("on_register"):
                session["username"] = username
                return redirect(
                    url_for(
                        "auth.validate_password"))
        
        # Verify if username is already exists
        except KeyError():
            return redirect("auth.register")
    
    return render_template("auth/validate_username.html")