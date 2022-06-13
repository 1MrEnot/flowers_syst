from dependency_injector.wiring import inject
from flask import Blueprint, render_template, request

import util
from models import *

view_bp = Blueprint('plant_view', __name__, url_prefix='/plants', template_folder="blueprints/")
api_bp = Blueprint('plant_api', __name__, url_prefix='/api/plant', template_folder="blueprints/")


@view_bp.route('/')
@inject
def plant_page():
    user_id = request.cookies.get(util.USER_ID_COOKIE)

    plants = [
        PlantModel(1, 'Plant1', None, 2),
        PlantModel(2, 'Plant2', 7, None),
        PlantModel(3, 'Plant3', 10, 0),
        PlantModel(4, 'Plant0', 0, 0),
    ]

    return render_template('plant.html', plants=plants)
