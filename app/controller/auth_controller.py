from flask import request
from flask_restx import Resource

from app.schema.auth.login_schema import LoginRequestSchema
from app.service.auth_service import user_login, logout_user, find_password
from app.dto.auth_dto import AuthDto
from app.util.constants import Constants
from app.util.decorator import token_required

api = AuthDto.api

_parser = api.parser()
_parser.add_argument("Authorization", location="headers", required=True)


@api.route("auth/login")
class Login(Resource):
    @api.expect(AuthDto.input_login, validate=True)
    @api.marshal_with(AuthDto.output_login)
    @api.doc(responses=Constants.RESPONSES)
    def post(self):
        """사용자 로그인"""
        req_data = LoginRequestSchema().load(request.json)
        return user_login(req_data.get('id'), req_data.get('password'))


@api.route("auth/logout")
class Logout(Resource):
    @token_required
    @api.expect(_parser, validate=True)
    @api.marshal_with(AuthDto.success)
    @api.doc(responses=Constants.RESPONSES)
    def get(self):
        """사용자 로그아웃"""
        return logout_user()


@api.route("auth/reset-password")
class ResetPassword(Resource):
    @api.expect(AuthDto.password_reset, validate=True)
    @api.marshal_with(AuthDto.success)
    @api.doc(responses=Constants.RESPONSES)
    def post(self):
        """비밀번호 리셋 (이메일 or SMS 발송)"""
        return find_password(request.json)
