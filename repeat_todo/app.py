import json

from flask import Flask

from repeat_todo.commands import lint, reinstall_db, test
from repeat_todo.extensions import db, login_manager, migrate
from repeat_todo.logger import configure_logger
from repeat_todo.models.user import User


def create_app(config_object="repeat_todo.settings"):
    """Create application factory.
    Refer: http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The config object to use
    :type config_object: str, optional
    """

    app = Flask("repeat_todo")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return None


def register_blueprints(app):
    """Register Flask blueprints."""

    from repeat_todo.views.auth_view import auth_route
    from repeat_todo.views.main_view import main_route
    from repeat_todo.views.task_template_view import task_template_route

    app.register_blueprint(main_route, url_prefix='/')
    app.register_blueprint(auth_route, url_prefix='/auth')
    app.register_blueprint(task_template_route, url_prefix='/task_template')

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
        return {"db": db}

    app.shell_context_processor(shell_context)

    return None


def register_commands(app):
    """Register Click commands."""

    app.cli.add_command(test)
    app.cli.add_command(lint)
    app.cli.add_command(reinstall_db)

    return None
