from flask import Flask, render_template

from blueprints.plants import view_bp as plant_view, api_bp as plant_api
from blueprints.user import view_bp as user_view, api_bp as user_api, bp as view
from container import Container


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__, static_folder='static')

    app.container = container
    app.register_blueprint(user_view)
    app.register_blueprint(user_api)
    app.register_blueprint(view)

    app.register_blueprint(plant_view)
    app.register_blueprint(plant_api)

    app.register_error_handler(404, error_handler_404)

    return app


def error_handler_404(e):
    return render_template('404.html')


if __name__ == '__main__':
    app = create_app()
    app.run()
