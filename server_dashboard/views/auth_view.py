import json

from flask import Blueprint, current_app, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from server_dashboard.utils import login_required, update_config

auth_route = Blueprint("auth", __name__)


@auth_route.route("/login", methods=["POST"])
def login():
    """Login a user."""
    data = json.loads(request.data)

    try:
        username = data["username"]
        password = data["password"]
    except KeyError:
        return jsonify({"error": "Missing username or password"}), 400

    users = current_app.config["DASHBOARD_CONFIG"]["users"]
    if username in users:
        if check_password_hash(users[username]["password"], password):
            session["username"] = username
            return jsonify({"message": "User logged in successfully."})
        else:
            return jsonify({"error": "Incorrect password"}), 400

    return jsonify({"error": "Username does not exist"}), 400


@auth_route.route("/signup", methods=["POST"])
def signup():
    """Signup a user."""
    data = json.loads(request.data)

    try:
        username = data["username"]
        password = data["password"]
    except KeyError:
        return jsonify({"error": "Missing username or password"}), 400

    users = current_app.config["DASHBOARD_CONFIG"]["users"]

    for user in users:
        if user["username"] == username:
            return jsonify({"error": "Username already exists"}), 400

    users[username] = {
        "password": generate_password_hash(password),
        "tiles": {},
    }

    current_app.config["DASHBOARD_CONFIG"]["users"] = users
    update_config(current_app.config["DASHBOARD_CONFIG"])

    return jsonify({"message": "User signed up successfully."})


@auth_route.route("/logout", methods=["POST"])
@login_required
def logout():
    """Logout a user."""
    session.pop("username", None)
    return jsonify({"message": "User logged out successfully."})
