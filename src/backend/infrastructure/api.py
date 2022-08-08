import pulumi
import pulumi_aws as aws
from pulumi_random.random_password import RandomPassword

from .common import domain, env, is_prod, project
from .components.container_function import Architecture, ContainerFunction
from .components.serverless_api import ServerlessApi
from .dns.certificate import certificate_validation
from .dns.zone import zone
from .repository import repository

secret_key = RandomPassword(resource_name="jwt-secret-key", length=50)

# GraphQL Lambda
graphql_function = ContainerFunction(
    name=f"{project}-graphql-{env}",
    description=f"{project} GraphQL function",
    build_and_push=True,
    timeout=30,
    keep_warm=True,
    architecture=Architecture.ARM64,
    repository=repository,
    dockerfile="Dockerfile",
    context=".",
    environment={  # type: ignore
        "POWERTOOLS_SERVICE_NAME": f"{project}-graphql",
        "STRIP_STAGE_PATH": "1",
        "SECRET_KEY": secret_key.result,
    },
)

# GraphQL API
graphql_api = ServerlessApi(
    name=f"{project}-graphql-{env}",
    description=f"Serverless HTTP API for {project} ({env})",
    function=graphql_function,
    cors_configuration=aws.apigatewayv2.ApiCorsConfigurationArgs(
        allow_origins=["*"] if not is_prod() else None,
        allow_headers=["authorization", "content-type"],
        allow_methods=["POST"],
    ),
    domain_name=f"api.{domain}",
    certificate_validation=certificate_validation,
    zone=zone,
)

pulumi.export("endpoint", graphql_api.endpoint)
