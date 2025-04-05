
from flask import render_template, Blueprint, session

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@main_bp.route("/index")
def index():
    return render_template("index.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/sss")
def sss():
    return render_template("sss.html")