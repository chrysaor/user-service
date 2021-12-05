from flask_restx import Model
from flask_restx.fields import String

from app.dto.user_dto import UserDto


def test_user_dto_user_info():
    current_model = UserDto.user_info

    assert isinstance(current_model, Model)
    assert len(current_model) == 4
    assert isinstance(current_model.get('email'), String)
    assert isinstance(current_model.get('name'), String)
    assert isinstance(current_model.get('nickname'), String)
    assert isinstance(current_model.get('mobile_num'), String)


def test_user_dto_register_sms_req():
    current_model = UserDto.register_sms_req.resolved

    assert isinstance(current_model, Model)
    assert len(current_model) == 5
    assert isinstance(current_model.get('sms_type'), String)
    assert isinstance(current_model.get('email'), String)
    assert isinstance(current_model.get('name'), String)
    assert isinstance(current_model.get('nickname'), String)
    assert isinstance(current_model.get('mobile_num'), String)


def test_user_dto_register_user():
    current_model = UserDto.register_user.resolved

    assert isinstance(current_model, Model)
    assert len(current_model) == 6
    assert isinstance(current_model.get('email'), String)
    assert isinstance(current_model.get('name'), String)
    assert isinstance(current_model.get('nickname'), String)
    assert isinstance(current_model.get('mobile_num'), String)
    assert isinstance(current_model.get('password'), String)
    assert isinstance(current_model.get('request_id'), String)
