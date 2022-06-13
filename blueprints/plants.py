from dependency_injector.wiring import inject
from flask import Blueprint, render_template

from models.Plant import PlantModel

view_bp = Blueprint('plant_view', __name__, url_prefix='/plants', template_folder="blueprints/")
api_bp = Blueprint('plant_api', __name__, url_prefix='/api/plant', template_folder="blueprints/")


@view_bp.route('/<plant_id>')
@inject
def plant_page(plant_id: int):
    plants = [
        PlantModel('Plant1', None, 2),
        PlantModel('Plant2', 7, None),
        PlantModel('Plant3', 10, 0),
        PlantModel('Plant0', 0, 0),

    ]

    return render_template('plant.html', plants=plants)
