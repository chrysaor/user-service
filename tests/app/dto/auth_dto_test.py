from flask_restx import Model
from flask_restx.fields import String

from app.dto.auth_dto import AuthDto


def test_auth_dto_input_login():
    current_model = AuthDto.input_login

    assert isinstance(current_model, Model)
    assert len(current_model) == 2
    assert isinstance(current_model.get('id'), String)
    assert isinstance(current_model.get('password'), String)


def test_auth_dto_output_login():
    current_model = AuthDto.output_login

    assert isinstance(current_model, Model)
    assert len(current_model) == 4
    assert isinstance(current_model.get('access_token'), String)
    assert isinstance(current_model.get('name'), String)
    assert isinstance(current_model.get('nickname'), String)
    assert isinstance(current_model.get('email'), String)


def test_auth_dto_success():
    current_model = AuthDto.success

    assert isinstance(current_model, Model)
    assert len(current_model) == 1
    assert isinstance(current_model.get('result'), String)


def test_auth_dto_password_reset():
    current_model = AuthDto.password_reset

    assert isinstance(current_model, Model)
    assert len(current_model) == 3
    assert isinstance(current_model.get('request_id'), String)
    assert isinstance(current_model.get('email'), String)
    assert isinstance(current_model.get('mobile_num'), String)
