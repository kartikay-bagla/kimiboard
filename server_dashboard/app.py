import json

from flask import Flask

from server_dashboard.commands import encrypt, lint, test
from server_dashboard.logger import configure_logger
from server_dashboard.utils import get_current_config


def create_app(config_object="server_dashboard.settings"):
    """Create application factory.
    Refer: http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The config object to use
    :type config_object: str, optional
    """

    app = Flask("server_dashboard")

    app.config.from_object(config_object)
    app.config["DASHBOARD_CONFIG"] = get_current_config()

    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)

    return app


def register_blueprints(app):
    """Register Flask blueprints."""

    from server_dashboard.views.auth_view import auth_route
    from server_dashboard.views.main_view import main_route
    from server_dashboard.views.tile_view import tile_route

    app.register_blueprint(main_route, url_prefix="/")
    app.register_blueprint(auth_route, url_prefix="/auth")
    app.register_blueprint(tile_route, url_prefix="/tile")

    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(e):
        """Render error template."""
        response = e.get_response()
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)

    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {}

    app.shell_context_processor(shell_context)

    return None


def register_commands(app):
    """Register Click commands."""

    app.cli.add_command(test)
    app.cli.add_command(lint)
    app.cli.add_command(encrypt)

    return None
