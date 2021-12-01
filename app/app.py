import os
import threading
import uuid
import flask_cors

from flask import Flask, Blueprint
from flask_gzip import Gzip
from flask_restx import Api

from app.database.models import init_db
from app.util.common import init_404_handler
from controller.health_controller import api as health_ns
from controller.auth_controller import api as auth_ns
from controller.user_controller import api as user_ns
from controller.sms_controller import api as sms_ns
from app.config.base import config_map

# Create Blueprint
blueprint = Blueprint(
    name="v1",
    import_name=__name__,
    url_prefix="/",
)

# Setting Bearer Authorization
authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    }
}

# Create API
api_tb = Api(
    blueprint,
    version="1",
    title="User service v1.0",
    description="User service API Document",
    contact="chrysaor@naver.com",
    prefix="/api",
    authorizations=authorizations,
    security="Bearer",
)


def create_app(config_name='development'):  # pragma: no cover
    print('=' * 80)
    print(f'CONFIG: {config_name}')
    print('-' * 80)

    # Flask application 생성 및 설정
    _app = Flask(__name__)
    _app.config.from_object(config_map[config_name])

    for k in sorted(_app.config.keys()):
        print(f'{k}\t{_app.config.get(k)}')

    print('=' * 80)

    @_app.before_request
    def pre_request():
        uuid4 = uuid.uuid4()
        thread = threading.current_thread()
        thread.request_id = uuid4
        print(uuid4)

    with _app.app_context():
        # Init database
        # DatabaseFactory.initialize(_app)
        init_db()

        # Setting cors
        flask_cors.CORS(
            _app, resources={r"*": {"origins": "*"}}
        )

        # Response Gzip 설정
        Gzip(_app)

        # default 404 json error 설정
        init_404_handler(_app)

        # Production Swagger Document 미생성 처리
        if config_name == 'production':
            api_tb.init_app(blueprint, add_specs=False)

        # Adding namespace
        api_tb.add_namespace(health_ns, '/')
        api_tb.add_namespace(user_ns, '/')
        api_tb.add_namespace(auth_ns, '/')
        api_tb.add_namespace(sms_ns, '/')

        _app.register_blueprint(blueprint)

    return _app


app = create_app(os.environ.get('FLASK_ENV', 'development'))
