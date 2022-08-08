from typing import Any, Dict

import serverless_wsgi
from aws_lambda_powertools.logging import Logger, correlation_paths
from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.utilities.data_classes import (
    APIGatewayProxyEventV2,
    event_source,
)
from aws_lambda_powertools.utilities.typing import LambdaContext

from .app import app

# Tracing & logging
# NB: remember to set the `POWERTOOLS_SERVICE_NAME` envvar in the Lambda
logger = Logger()
tracer = Tracer()


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
@event_source(data_class=APIGatewayProxyEventV2)
def lambda_handler(
    event: APIGatewayProxyEventV2, context: LambdaContext
) -> Dict[str, Any]:
    """Main AWS λ handler for this project.

    All this does is validate the incoming payload via the `event_source` decorator
    then send the event body to `serverless_wsgi` which will translate the JSON event
    into a Python WSGI Request which can then be processed by the Flask `app`.

    We're using Flask here instead of λ powertools' resolver because Flask can be
    executed locally.

    Args:
        event (APIGatewayProxyEventV2): An HTTP API incoming JSON event
        context (LambdaContext): The AWS λ context

    Returns:
        Dict[str, Any]: A JSON response containing a status code, a payload and possibly
                        error messages in case of an Exception.
    """
    response: Dict[str, Any] = serverless_wsgi.handle_request(
        app=app, event=event.raw_event, context=context
    )
    return response
