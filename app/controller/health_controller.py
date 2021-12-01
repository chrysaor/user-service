from flask_restx import Resource

from app.dto.health_dto import HealthDto
from app.service.health_service import get_health_check

from app.util.constants import Constants


api = HealthDto.api


@api.route("health-check")
class HealthCheck(Resource):
    @api.marshal_with(HealthDto.health_check, envelope="data")
    @api.doc(responses=Constants.RESPONSES)
    def get(self):
        """
        Health check API
        """
        return get_health_check()
