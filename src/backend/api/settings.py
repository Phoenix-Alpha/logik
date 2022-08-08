import os
from typing import Optional

DEBUG: bool = bool(os.environ.get("DEBUG", 1))

FAKER_LOCALE: str = os.environ.get("FAKER_LOCALE", "fr_FR")

AWS_REGION: str = os.environ.get("AWS_REGION", "eu-west-1")
AWS_ACCESS_KEY_ID: str = os.environ.get("AWS_ACCESS_KEY_ID", "DUMMYAWSACCESSKEYID")
AWS_SECRET_ACCESS_KEY: str = os.environ.get(
    "AWS_SECRET_ACCESS_KEY", "DUMMYAWSSECRETACCESSKEY"
)
DYNAMODB_ENDPOINT_URL: Optional[str] = os.environ.get(
    "DYNAMODB_ENDPOINT_URL", "http://localhost:8001"
)
STEPFUNCTIONS_ENDPOINT_URL: Optional[str] = os.environ.get("STEPFUNCTIONS_ENDPOINT_URL")

# Tables

INTEGRATOR_TABLE_NAME = "Integrator"

# Authentication

JWT_SECRET: str = os.environ["SECRET_KEY"]
JWT_ISSUER: str = "logik"

# API Key

SUPERADMIN_API_KEY = "lgk_f5e9874c6ee4"
