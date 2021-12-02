from flask import Flask

from .resources.documentation.blueprint import blueprint as blueprint_documentation

# Import blueprints
from .resources.user.blueprint import blueprint as blueprint_user


def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(blueprint_user)
    app.register_blueprint(blueprint_documentation)

    return app


app = create_app()
