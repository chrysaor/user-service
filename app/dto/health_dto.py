from flask_restx import Namespace, fields


class HealthDto:
    """
    Health Check DTO
    """
    api = Namespace("health", description="health check")

    health_check = api.model(
        "health_check",
        {
            "health_check": fields.Boolean(
                default=True,
                description="health check",
                attribute="health_check",
            ),
        },
    )
