from flask import Blueprint, redirect, render_template
from flask_login import current_user, login_required, logout_user

from server_dashboard.models.tile import Tile

main_route = Blueprint("main", __name__)


@main_route.route("/", methods=["GET"])
@login_required
def index():
    """Render the main dashboard."""
    tiles = Tile.query.filter_by(user_id=current_user.id).all()
    tiles = [tile.as_dict for tile in tiles]
    print(tiles)
    return render_template("index.html", tiles=tiles)


@main_route.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect("/")
    return render_template("login.html")


@main_route.route("/signup")
def signup():
    if current_user.is_authenticated:
        return redirect("/")
    return render_template("signup.html")


@main_route.route("/logout")
def logout():
    logout_user()
    return redirect("/login")
