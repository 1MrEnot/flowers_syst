from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template, request

import util
from container import Container
from services.Repository import Repository

view_bp = Blueprint('plant_view', __name__, url_prefix='/plants', template_folder="blueprints/")


@view_bp.route('/')
@inject
def plant_page(repository: Repository = Provide[Container.repository]):
    user_id = int(request.cookies.get(util.USER_ID_COOKIE))
    user = repository.get_user_info(user_id)
    return render_template('plant.html', plants=user.plants)
