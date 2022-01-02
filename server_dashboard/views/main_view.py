from flask import Blueprint, current_app, redirect, render_template, session

from server_dashboard.utils import login_required

main_route = Blueprint("main", __name__)


@main_route.route("/", methods=["GET"])
@login_required
def index():
    config = current_app.config["DASHBOARD_CONFIG"]
    username = session["username"]
    tiles = config["users"][username]["tiles"]
    return render_template("index.html", tiles=tiles)


@main_route.route("/login")
def login():
    if session.get("username"):
        return redirect("/")
    return render_template("login.html")


@main_route.route("/signup")
def signup():
    if session.get("username"):
        return redirect("/")
    return render_template("signup.html")


@main_route.route("/logout")
def clear_sessions():
    session.clear()
    return redirect("/login")


# @main_route.route("/get-config")
# def get_config_endpoint():
#     return jsonify(current_app.config["DASHBOARD_CONFIG"])


# @main_route.route("/update-config", methods=["POST"])
# def update_config_endpoint():
#     data = request.get_json()
#     current_app.config["DASHBOARD_CONFIG"] = data
#     update_config(data)
