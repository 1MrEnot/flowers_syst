from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request, render_template, jsonify, make_response, redirect

import util
from container import Container
from models import *
from services.Repository import Repository

view_bp = Blueprint('user_view', __name__, url_prefix='/user', template_folder="blueprints/")
api_bp = Blueprint('user_api', __name__, url_prefix='/api/user', template_folder="blueprints/")
bp = Blueprint('api', __name__, template_folder="blueprints/")


@bp.route('/')
@inject
def index():
    user_id = request.cookies.get(util.USER_ID_COOKIE)
    if user_id is None:
        return render_template('login.html')

    return redirect('/user')


@view_bp.route('/')
@inject
def user_page(repository: Repository = Provide[Container.repository]):
    try:
        user_id = request.cookies.get(util.USER_ID_COOKIE)
        user = repository.get_user_info(int(user_id))
        return render_template(
            'profile.html',
            name=user.name,
            email=user.email,
            plant_count=len(user.plants),
            winter_mode=user.is_winter_mode
        )
    except:
        return redirect('/')


@api_bp.post('/')
@inject
def create_user(repository: Repository = Provide[Container.repository]):
    try:
        data: dict = request.get_json()
        username = data.get('name', None)
        password = data.get('password', None)
        email = data.get('email', None)

        if not (username and email and password):
            return {'error': "Укажите имя, email и пароль"}, 422

        repository.create_user(UserCreateRequest(username, email, password))
        return 'OK', 200

    except Exception as e:
        return {'error': str(e)}, 419


@api_bp.get('/<user_id>')
@inject
def get_user(user_id: int, repository: Repository = Provide[Container.repository]):
    user = repository.get_user_info(user_id)
    as_dict = dataclasses.asdict(user, dict_factory=util.dataclass_dict_factory)
    res = jsonify(as_dict)
    return res


@bp.post('/login')
@inject
def login(repository: Repository = Provide[Container.repository]):
    data: dict = request.get_json()
    login = data['login']
    password = data['password']
    user = repository.authenticate(login, password)
    if not user:
        return {'error': 'Нет такого пользователя'}, 401

    response = make_response(jsonify({'redirect': '/user'}))
    response.set_cookie(util.USER_ID_COOKIE, str(user.u_id))
    return response
