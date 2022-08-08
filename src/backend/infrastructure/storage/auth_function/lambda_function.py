"""
Lambda handler that manages authentication between an AWS Transfer FTP server and
our GraphQL API

https://docs.aws.amazon.com/transfer/latest/userguide/custom-identity-provider-users.html#authentication-lambda-examples
"""

import json
import os
from enum import Enum
from typing import Any, Dict, List, Optional

from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.utilities.parser import BaseModel, Field, event_parser
from aws_lambda_powertools.utilities.typing import LambdaContext

# Tracing & logging
# NB: remember to set the `POWERTOOLS_SERVICE_NAME` envvar in the Lambda
logger = Logger()
tracer = Tracer()

TRANSFER_ACCESS_ROLE_ARN = os.environ["TRANSFER_ACCESS_ROLE_ARN"]
TRANSFER_BUCKET_NAME = os.environ["TRANSFER_BUCKET_NAME"]
TRANSFER_BUCKET_ARN = f"arn:aws:s3:::{TRANSFER_BUCKET_NAME}"


class HomeDirectoryDetail(BaseModel):
    Entry: str
    Target: str


class HomeDirectoryType(str, Enum):
    LOGICAL = "LOGICAL"
    PATH = "PATH"


class TransferAuthResponse(BaseModel):
    Role: Optional[str] = Field(
        description=(
            "The user will be authenticated if and only if the Role field is not blank"
        )
    )
    PosixProfile: Optional[str] = Field(
        description="Required for Amazon EFS backing storage",
        default=None,
    )
    PublicKeys: Optional[List[str]] = []
    Policy: Optional[str] = None
    HomeDirectoryType: HomeDirectoryType
    HomeDirectoryDetails: Optional[str] = Field(
        description="Required if HomeDirectoryType has a value of LOGICAL",
        default=None,
    )
    HomeDirectory: Optional[str] = Field(
        description="Required if HomeDirectoryType has a value of PATH",
        default=None,
    )


class TransferProtocol(str, Enum):
    FTP = "FTP"
    SFTP = "SFTP"
    FTPS = "FTPS"


class TransferAuthEvent(BaseModel):
    username: str
    password: Optional[str] = None
    serverId: str
    sourceIp: str
    protocol: TransferProtocol


@logger.inject_lambda_context  # type: ignore
@tracer.capture_lambda_handler  # type: ignore
@event_parser(model=TransferAuthEvent)  # type: ignore
def lambda_handler(event: TransferAuthEvent, context: LambdaContext) -> Dict[str, Any]:
    if event.password:
        print(f"Password authentication for {event.username}")
        if event.username == "jdoe" and event.password == "1234":
            workspace = "toto"
            response = TransferAuthResponse(
                HomeDirectoryType=HomeDirectoryType.LOGICAL,
                HomeDirectoryDetails=json.dumps(
                    [
                        HomeDirectoryDetail(
                            Entry=f"/{workspace}",
                            Target=f"/{TRANSFER_BUCKET_NAME}/{workspace}",
                        ).dict()
                    ]
                ),
                Role=TRANSFER_ACCESS_ROLE_ARN,
                Policy=json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Sid": "AllowListAccessToBucket",
                                "Action": ["s3:ListBucket"],
                                "Effect": "Allow",
                                "Resource": [TRANSFER_BUCKET_ARN],
                                "Condition": {
                                    "StringLike": {
                                        "s3:prefix": [
                                            f"{workspace}",
                                            f"{workspace}/*",
                                        ]
                                    }
                                },
                            },
                            {
                                "Sid": "TransferDataBucketAccess",
                                "Effect": "Allow",
                                "Action": [
                                    "s3:PutObject",
                                    "s3:PutObjectAcl",
                                    "s3:GetObject",
                                    "s3:GetObjectAcl",
                                    "s3:GetObjectVersion",
                                    "s3:GetBucketLocation",
                                    "s3:DeleteObject",
                                    "s3:DeleteObjectVersion",
                                ],
                                "Resource": [
                                    f"{TRANSFER_BUCKET_ARN}/{workspace}",
                                    f"{TRANSFER_BUCKET_ARN}/{workspace}/*",
                                ],
                            },
                        ],
                    }
                ),
            )
            return response.dict()
        else:
            # Return HTTP status 200 but with no role in the response to indicate
            # authentication failure
            return {}
    elif event.protocol == TransferProtocol.SFTP:
        print(f"Public key SFTP authentication for {event.username}")
        # TODO: implement passwordless auth (?)
        # import boto3
        # s3 = boto3.client("s3")  # type: ignore
        # s3.get_object()
        return {}
    else:
        # Return HTTP status 200 but with no role in the response to indicate
        # authentication failure
        return {}
