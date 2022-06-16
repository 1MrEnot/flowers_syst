from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from blueprints.plants import view_bp as plant_view
from blueprints.plots import view_bp as plot_view, api_bp as plot_api
from blueprints.user import view_bp as user_view, api_bp as user_api, bp as view
from container import Container, URL
from entities import Base


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__, static_folder='static')

    app.container = container
    app.register_blueprint(view)
    app.register_blueprint(user_view)
    app.register_blueprint(plant_view)
    app.register_blueprint(plot_view)

    app.register_blueprint(user_api)
    app.register_blueprint(plot_api)

    app.register_error_handler(404, error_handler_404)

    if not database_exists(URL):
        create_database(URL)
        engine = create_engine(URL)
        Base.metadata.create_all(engine)

    return app


def error_handler_404(e):
    return render_template('404.html')


if __name__ == '__main__':
    app = create_app()
    app.run()
