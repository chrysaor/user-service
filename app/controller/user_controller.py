from flask import request
from flask_restx import Resource

from app.dto.user_dto import UserDto
from app.service.auth_service import get_logged_in_user
from app.service.user_service import create_user
from app.util.constants import Constants
from app.util.decorator import token_required

api = UserDto.api
_parser = api.parser()


@api.route("users")
class User(Resource):
    @token_required
    @api.expect(_parser, validate=True)
    @api.marshal_with(UserDto.user_info)
    @api.doc(responses=Constants.RESPONSES)
    def get(self):
        """ 회원 정보 조회 (본인) """
        return get_logged_in_user()

    @api.expect(UserDto.register_user, validate=True)
    @api.marshal_with(UserDto.user_info)
    @api.doc(responses=Constants.RESPONSES)
    def post(self):
        """ 회원 가입 """
        return create_user(request.json)
