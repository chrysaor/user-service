from flask import request
from flask_restx import Resource

from app.dto.sms_dto import SmsDto
from app.dto.user_dto import UserDto
from app.service.sms_service import sms_request, sms_request_validation
from app.util.constants import Constants

api = SmsDto.api
_parser = api.parser()


@api.route("sms")
class SmsRequest(Resource):
    @api.expect(UserDto.register_sms_req, validate=True)
    @api.doc(responses=Constants.RESPONSES)
    def post(self):
        """ SMS 인증 요청 """
        return sms_request(request.json)


@api.route("sms/validation")
class SmsRequestValidation(Resource):
    @api.expect(SmsDto.validation_req, validate=True)
    @api.doc(responses=Constants.RESPONSES)
    def post(self):
        """ SMS 인증 번호 확인 """
        return sms_request_validation(request.json)
