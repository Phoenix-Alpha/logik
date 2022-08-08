import json
from datetime import datetime
from enum import Enum
from typing import Optional

import boto3
import strawberry

from ... import settings
from ...permissions import IsAuthenticated
from ...scalars import JSONScalar
from .graphql_types import Edge, Flow, Task
from .providers import fake

dynamodb = boto3.resource(
    "dynamodb",
    region_name=settings.AWS_REGION,
    endpoint_url=settings.DYNAMODB_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)
sfn = boto3.client(
    "stepfunctions",
    region_name=settings.AWS_REGION,
    endpoint_url=settings.STEPFUNCTIONS_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

# Create Flow


@strawberry.input
class CreateFlowInput:
    pass


# Flow execution


@strawberry.enum
class FlowExecutionStatus(str, Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    TIMED_OUT = "timed_out"


@strawberry.type
class FlowExecutionResult:
    start_date: datetime
    end_date: datetime
    status: FlowExecutionStatus
    input: JSONScalar
    output: JSONScalar
    error_code: Optional[str]
    error_message: Optional[str]


# Mutation


@strawberry.type
class FlowManagerMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_flow(self, name: str, description: Optional[str]) -> Flow:
        return Flow(
            id=fake.id(),
            name=name,
            description=description,
            edges=[
                Edge(
                    source=Task(function_id=fake.id()),
                    target=Task(function_id=fake.id()),
                )
            ],
        )

    @strawberry.mutation(
        description="Executes a given flow", permission_classes=[IsAuthenticated]
    )
    def execute_flow(
        self,
        id: str = strawberry.field(description="ID of a Flow"),
        input: JSONScalar = strawberry.field(description="A JSON payload"),
    ) -> FlowExecutionResult:
        """Runs a given Flow synchroneously

        Returns:
            str: [description]

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.start_sync_execution
        """
        flow_table = dynamodb.Table("Flow")
        response = flow_table.get_item(Key={"id": id})
        object = response["Item"]
        # Execute the Step Function
        result = sfn.start_sync_execution(
            stateMachineArn=str(object["step_function_arn"]),
            input=json.dumps(input),
        )
        return FlowExecutionResult(
            input=input,
            output=result["output"],
            start_date=result["startDate"],
            end_date=result["stopDate"],
            status=FlowExecutionStatus(result["status"]),
            error_code=result["error"],
            error_message=result["cause"],
        )
