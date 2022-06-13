from flask import Blueprint, request, render_template
from dependency_injector.wiring import Provide, inject

from services.UserService import UserService
from container import Container


view_bp = Blueprint('user_view', __name__, url_prefix='/user', template_folder="blueprints/")
api_bp = Blueprint('user_api', __name__, url_prefix='/api/user', template_folder="blueprints/")


@view_bp.route('/<user_id>')
@inject
def user_page(user_id: int,
              user_service: UserService = Provide[Container.user_service]):
    user = user_service.get_user_info(user_id)
    return render_template('login.html', name=user.email, plant_count=user.plant_count, winter_mode=user.is_winter_mode)


@api_bp.post('/')
@inject
def create_user():
    data: dict = request.get_json()
    return 'OK', 200
