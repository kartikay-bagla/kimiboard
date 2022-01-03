import json

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from server_dashboard.extensions import db
from server_dashboard.models.tile import Tile

tile_route = Blueprint("tile", __name__)


@tile_route.route("/", methods=["GET"])
@login_required
def get_tiles():
    """Get all tiles."""
    tiles = Tile.query.filter_by(user_id=current_user.id).all()
    return jsonify([tile.as_dict for tile in tiles])


@tile_route.route("/", methods=["POST"])
@login_required
def create_tile():
    """Create a new tile."""
    data = json.loads(request.data)

    try:
        name = data["name"]
        url = data["url"]
        icon = data["icon"]
    except KeyError:
        return jsonify({"error": "Missing name, url or icon"}), 400

    tile = Tile(name=name, url=url, icon=icon, user_id=current_user.id)
    db.session.add(tile)
    db.session.commit()
    return jsonify({"message": "Tile created successfully."})


@tile_route.route("/<int:tile_id>", methods=["GET"])
@login_required
def get_tile(tile_id):
    """Get a tile by id."""
    tile = Tile.query.filter_by(id=tile_id, user_id=current_user.id).first()
    return jsonify(tile.as_dict)


@tile_route.route("/<int:tile_id>", methods=["PUT"])
@login_required
def update_tile(tile_id):
    """Update a tile."""
    data = json.loads(request.data)

    try:
        name = data["name"]
        url = data["url"]
        icon = data["icon"]
    except KeyError:
        return jsonify({"error": "Missing name, url or icon"}), 400

    tile = Tile.query.filter_by(id=tile_id, user_id=current_user.id).first()
    if not tile:
        return jsonify({"error": "Tile does not exist"}), 400

    tile.name = name
    tile.url = url
    tile.icon = icon
    db.session.commit()
    return jsonify({"message": "Tile updated successfully."})


@tile_route.route("/<int:tile_id>", methods=["DELETE"])
@login_required
def delete_tile(tile_id):
    """Delete a tile."""
    tile = Tile.query.filter_by(id=tile_id, user_id=current_user.id).first()
    if not tile:
        return jsonify({"error": "Tile does not exist"}), 400

    db.session.delete(tile)
    db.session.commit()
    return jsonify({"message": "Tile deleted successfully."})
