# MANAGE APP.PY URLs
from flask import Blueprint, render_template, url_for

auth_bp = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

@auth_bp.route("/")
def index():
    return render_template("index.html")