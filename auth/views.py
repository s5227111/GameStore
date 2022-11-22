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

@auth_bp.route("/email-validation", methods=["POST", "GET"])
def email_validation():
    
    # Verify if email is already exists 
    email_exists = False
    if request.method == "POST":
        try:
            email = request.form.get("email")

            # Verify if email is already exists
            user = UserQuery.get_user_by_email(email)
            if user:
                email_exists = True 
                return render_template(
                    "auth/register-email-validation.html", 
                    email_exists=email_exists
                    )
            session["email"] = email
            session["on_register"] = True
            
            return redirect(
                url_for(
                    "auth.register_username_validation"))

        except KeyError():
            return redirect("auth.register")

    return render_template("auth/register-email-validation.html")

@auth_bp.route("/username-validation", methods=["POST", "GET"])
def username_validation():

    username_exists = False

    if request.method == "POST":
        try:
            username = request.form.get("username")

            # Verify if username is already exists
            user = UserQuery.get_user_by_username(username)


            if user:
                username_exists = True 
                return render_template(
                    "auth/register-username-validation.html", 
                    username_exists=username_exists
                    )
            
            # Verify if session has email and if user has validated email
            if session.get("email") and session.get("on_register"):
                session["username"] = username
                return redirect(
                    url_for(
                        "auth.register_password_validation"))
        
        # Verify if username is already exists
        except KeyError():
            return redirect("auth.register")
    
    return render_template("auth/register-username-validation.html")