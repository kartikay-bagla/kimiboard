from flask import Blueprint, current_app, jsonify, request, session

from server_dashboard.utils import login_required, update_config

tile_route = Blueprint("tile", __name__)


@tile_route.route("/delete", methods=["POST"])
@login_required
def delete():
    data = request.get_json()
    username = session["username"]

    config = current_app.config["DASHBOARD_CONFIG"]
    tiles = config["users"][username]["tiles"]

    if data["name"] not in tiles:
        return jsonify({"error": "Tile does not exist"}), 400

    del tiles[data["name"]]
    update_config(config)

    return jsonify({"message": "Tile deleted successfully."})


@tile_route.route("/add", methods=["POST"])
@login_required
def add():
    data = request.get_json()
    username = session["username"]

    config = current_app.config["DASHBOARD_CONFIG"]
    tiles = config["users"][username]["tiles"]

    try:
        name = data["name"]
        url = data["url"]
        icon = data["icon"]
    except KeyError:
        return jsonify({"error": "Missing name, url or icon"}), 400

    if name in tiles:
        return jsonify({"error": "Tile already exists"}), 400

    tiles[name] = {
        "url": url,
        "icon": icon,
    }
    update_config(config)

    return jsonify({"message": "Tile added successfully."})


@tile_route.route("/update", methods=["POST"])
@login_required
def update():
    data = request.get_json()
    username = session["username"]

    config = current_app.config["DASHBOARD_CONFIG"]
    tiles = config["users"][username]["tiles"]

    try:
        old_name = data["oldName"]
        name = data["name"]
        url = data["url"]
        icon = data["icon"]
    except KeyError:
        return jsonify({"error": "Missing name, oldName, url or icon"}), 400

    if old_name not in tiles:
        return jsonify({"error": "Tile does not exist"}), 400

    del tiles[old_name]
    tiles[name] = {
        "url": url,
        "icon": icon,
    }
    update_config(config)

    return jsonify({"message": "Tile updated successfully."})
