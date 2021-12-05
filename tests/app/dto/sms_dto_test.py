from flask_restx import Model
from flask_restx.fields import String

from app.dto.sms_dto import SmsDto


def test_sms_dto_validation_req():
    current_model = SmsDto.validation_req

    assert isinstance(current_model, Model)
    assert len(current_model) == 4
    assert isinstance(current_model.get('sms_type'), String)
    assert isinstance(current_model.get('request_id'), String)
    assert isinstance(current_model.get('mobile_num'), String)
    assert isinstance(current_model.get('auth_code'), String)
