# MANAGE APP.PY URLs
from flask import Blueprint, render_template, url_for

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

@auth_bp.route("/")
def index():
    return render_template("auth/index.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    return render_template("auth/register.html")