from flask_restx import Model
from flask_restx.fields import Boolean

from app.dto.health_dto import HealthDto


def test_health_dto_health_check():
    current_model = HealthDto.health_check

    assert isinstance(current_model, Model)
    assert len(current_model) == 1
    assert isinstance(current_model.get('health_check'), Boolean)
