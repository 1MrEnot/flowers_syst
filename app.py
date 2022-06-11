from blueprints.user import view_bp as user_view, api_bp as user_api

from flask import Flask
from container import Container, URL


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__, static_folder='static')
    app.config['SQLALCHEMY_DATABASE_URI'] = URL

    app.container = container
    app.register_blueprint(user_view)
    app.register_blueprint(user_api)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
