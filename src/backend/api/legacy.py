import json
import os
import secrets
from time import time
from typing import Any, Dict

import boto3
import jwt
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
from mypy_boto3_dynamodb.type_defs import QueryOutputTypeDef
from strawberry.permission import BasePermission

from . import settings

dynamodb = boto3.resource(
    "dynamodb",
    region_name=settings.AWS_REGION,
    endpoint_url=settings.DYNAMODB_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

DEFAULT_ISSUER = "nuage-logik"
DEFAULT_JWT_ID_AUDIENCE = "nuage-logik-graphql"
JWT_AUTH_TOKEN_EXPIRY = 60 * 60  # 1 hour
JWT_REFRESH_TOKEN_EXPIRY = 60 * 60 * 24 * 28  # 28 days


def generate_jwt(claims: Dict[str, Any]) -> str:
    JWT_DEFAULT_EXPIRY = (
        15 * 60
    )  # 15 minutes, short enough to protect us in case a user's token gets compromised
    JWT_REFRESH_TOKEN_EXPIRY = 60 * 60 * 24 * 28  # 28 days
    return jwt.encode(payload=claims, key="$ecret")


load_dotenv()
load_dotenv(dotenv_path="key.env")


def get_configuration():
    def require_env(name: str) -> None:
        if os.environ.get(name) is None:
            raise ValueError(
                f"Missing environment variable: {name}.  "
                "You can generate keys for development with `task generate-keys`"
            )

    require_env("ID_KEY_PAIR")
    require_env("REFRESH_KEY_PAIR")

    id_key_pair = json.loads(os.environ.get("ID_KEY_PAIR"))
    refresh_key_pair = json.loads(os.environ.get("REFRESH_KEY_PAIR"))

    id_public_key = {k: id_key_pair[k] for k in ["kty", "e", "use", "alg", "n", "kid"]}
    refresh_public_key = {
        k: refresh_key_pair[k] for k in ["kty", "e", "use", "alg", "n", "kid"]
    }

    issuer = get_env("JWT_ISSUER", DEFAULT_ISSUER)
    id_audience = get_env("JWT_ID_AUDIENCE", DEFAULT_JWT_ID_AUDIENCE)
    id_expiry = int(get_env("JWT_ID_EXPIRY", DEFAULT_JWT_ID_EXPIRY))
    refresh_expiry = int(get_env("JWT_REFRESH_EXPIRY", DEFAULT_JWT_REFRESH_EXPIRY))

    return {
        "id_key_pair": id_key_pair,
        "refresh_key_pair": refresh_key_pair,
        "id_public_key": id_public_key,
        "refresh_public_key": refresh_public_key,
        "issuer": issuer,
        "id_audience": id_audience,
        "id_expiry": id_expiry,
        "refresh_expiry": refresh_expiry,
    }


def generate_jwt(key_pair, claims, expiry_seconds):
    """
    Generates a JWT with the given claims.  The `iat`, `nbf` and `exp` claims are all
    generated from the current time and the `expiry` argument.
    """
    current_time = int(time())

    payload = {
        **claims,
        "iat": current_time,
        "nbf": current_time,
        "exp": current_time + expiry_seconds,
    }
    header = {
        "alg": key_pair.get("alg"),
        "kid": key_pair.get("kid"),
    }

    return jwt.encode(
        headers=header,
        claims=payload,
        algorithm=key_pair.get("alg"),
        key=key_pair,
    )


def generate_id_token_for_user(sub, claims={}):
    """
    Generates an ID token for the given user.  Optionally, a set of
    claims to be encoded in the token can also be given.
    """
    config = get_configuration()

    return generate_jwt(
        key_pair=config["id_key_pair"],
        claims={
            **claims,
            "aud": config["id_audience"],
            "iss": config["issuer"],
            "sub": str(sub),
        },
        expiry_seconds=config["id_expiry"],
    )


def generate_refresh_token_for_user(sub, claims={}):
    """
    Generates a refresh token for the given user.  Optionally, a set of
    claims to be encoded in the token can also be given.
    """
    config = get_configuration()

    return generate_jwt(
        key_pair=config["refresh_key_pair"],
        claims={
            **claims,
            "iss": config["issuer"],
            "sub": str(sub),
        },
        expiry_seconds=config["refresh_expiry"],
    )


def get_token_claims(token):
    return jwt.get_unverified_claims(token)


def validate_id_token(token):
    """
    Validates an ID token and returns the payload.
    """
    config = get_configuration()
    unverified_header = jwt.get_unverified_header(token)

    key = config["id_public_key"]

    if unverified_header["kid"] != key["kid"]:
        raise ValueError("JWT kid not recognized")

    return jwt.decode(
        token,
        key,
        algorithms=[key["alg"]],
        issuer=config["issuer"],
        audience=config["id_audience"],
    )


def validate_refresh_token(token):
    """
    Validates a refresh token.
    """
    config = get_configuration()
    unverified_header = jwt.get_unverified_header(token)
    key = config["refresh_public_key"]

    if unverified_header["kid"] != key["kid"]:
        raise ValueError("JWT kid not recognized")

    return jwt.decode(
        token,
        key,
        algorithms=[key["alg"]],
        issuer=config["issuer"],
    )


def refresh_tokens(refresh_token):
    """
    Given a valid refresh token, return a new ID token
    """
    claims = validate_refresh_token(refresh_token)
    return {
        "id_token": generate_id_token_for_user(sub=claims["sub"], claims=claims),
        "refresh_token": generate_refresh_token_for_user(
            sub=claims["sub"], claims=claims
        ),
    }


def generate_tokens(integrator_name: str, environment_id: str) -> JWT:
    sub: str = f"{integrator_name}_{environment_id}"
    claims = {"integrator_name": integrator_name, "environment_id": environment_id}
    return JWT(
        id_token=generate_id_token_for_user(sub=sub, claims=claims),
        refresh_token=generate_refresh_token_for_user(sub=sub, claims=claims),
    )


def login(api_key: str) -> LoginOutput:
    """
    Description: Performs a login with API key. If not provided or API key does not
    exist, returns LoginError. Otherwise returns LoginSuccess with JWT
    """

    current_time = int(time())

    if not api_key:
        return LoginOutput(result=LoginError(message="API key missing."))

    integrator_table = dynamodb.Table(name="IntegratorModel")
    query_response = integrator_table.query(
        IndexName="GSI_API_KEY_INDEX", KeyConditionExpression=Key("api_key").eq(api_key)
    )

    if query_response["Count"] != 1:
        return LoginOutput(result=LoginError(message="Invalid API key!"))
    else:
        existing_integrator: IntegratorModel = IntegratorModel(
            **query_response["Items"][0]
        )
        if existing_integrator.api_key_expires_at < current_time:
            return LoginOutput(result=LoginError(message="This API key is expired."))

        if (
            existing_integrator.integrator_name is None
            or existing_integrator.environment_id is None
        ):
            return LoginOutput(result=LoginError(message="Invalid API key!"))

        return LoginOutput(
            result=LoginSuccess(
                jwt_token=generate_tokens(
                    integrator_name=existing_integrator.integrator_name,
                    environment_id=existing_integrator.environment_id,
                )
            )
        )


def register_integrator(input: RegisterIntegratorInput) -> RegisterIntegratorOutput:
    """
    Description: Register integrator with name and email
    Input: RegisterIntegratorInput
    Output: RegisterIntegratorOuput
    """

    current_time = int(time())

    # Input validation

    if not input.integrator_name or not input.email:
        return RegisterIntegratorOutput(
            result=RegisterIntegratorError(message="Required fields empty!")
        )

    # Check if the integrator name exists

    integrator_table = dynamodb.Table(name="IntegratorModel")

    query_response: QueryOutputTypeDef = integrator_table.query(
        KeyConditionExpression=Key("integrator_name").eq(input.integrator_name)
    )

    if query_response["Count"] > 0:
        return RegisterIntegratorOutput(
            result=RegisterIntegratorError(
                message=(
                    "Integrator with this name already registered. Please try a "
                    "different name."
                )
            )
        )

    default_environment_name = "development"
    default_environment_id: str = generate_environment_id()

    api_key: str = generate_api_key(
        integrator_name=input.integrator_name, environment_id=default_environment_id
    )

    try:
        integrator_table.put_item(
            Item={
                "integrator_name": input.integrator_name,
                "email": input.email,
                "email_verified": False,
                "status": IntegratorStatus.ACTIVE,
                "environment_id": default_environment_id,
                "environment_name": default_environment_name,
                "environment_status": EnivronmentStatus.ACTIVE,
                "api_key": api_key,
                "last_login_at": current_time,
                "created_at": current_time,
                "updated_at": current_time,
            }
        )
    except BaseException:
        return RegisterIntegratorOutput(
            result=RegisterIntegratorError(
                message="Sorry, integrator registration failed. Please try again."
            )
        )

    return RegisterIntegratorOutput(
        result=RegisterIntegratorSuccess(
            jwt_token=generate_tokens(
                input.integrator_name, environment_id=default_environment_id
            )
        )
    )
