import dataclasses
import datetime

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template, request, jsonify

import util
from container import Container
from models import Moisture
from services.Repository import Repository


view_bp = Blueprint('plot_view', __name__, url_prefix='/plots', template_folder="blueprints/")
api_bp = Blueprint('plot_api', __name__, url_prefix='/api/plots', template_folder="blueprints/")


@view_bp.route('/')
@inject
def plot_page(repository: Repository = Provide[Container.repository]):
    user_id = int(request.cookies.get(util.USER_ID_COOKIE))
    user = repository.get_user_info(user_id)
    return render_template('schedule.html', plants=user.plants)


@api_bp.get('/<plant_id>')
@inject
def plot_page(plant_id: int, repository: Repository = Provide[Container.repository]):
    plant_info = repository.get_plant_info(plant_id)
    plant_info.forecast = _get_fake_forecast(plant_info)
    as_dict = dataclasses.asdict(plant_info, dict_factory=util.dataclass_dict_factory)
    return jsonify(as_dict)


def _get_fake_forecast(plant_info, step=-0.05):
    last_value = plant_info.measurements[-1].value
    last_time = plant_info.measurements[-1].timestamp

    res = [Moisture(last_value + i * step, last_time + datetime.timedelta(hours=i)) for i in range(4)]
    return res



