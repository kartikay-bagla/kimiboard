import json
from functools import wraps

from flask import current_app, redirect, session


def get_current_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config


def update_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    current_app.config["DASHBOARD_CONFIG"] = config
    return None


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username"):
            return func(*args, **kwargs)
        else:
            return redirect("/login")

    return wrapper
