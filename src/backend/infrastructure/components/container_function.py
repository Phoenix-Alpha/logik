import base64
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, Optional, Union

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker
import pulumi_docker_buildkit as buildx


class Architecture(IntEnum):
    """CPU architecture & instruction set to use"""

    X86_64 = 1
    ARM64 = 2

    @property
    def lambda_value(self) -> str:
        """AWS Lambda value for the `architectures` argument"""
        mapping = {self.X86_64.value: "x86_64", self.ARM64.value: "arm64"}
        return mapping[self.value]

    @property
    def docker_value(self) -> str:
        """Docker value for the `--platform` flag"""
        mapping = {self.X86_64.value: "linux/amd64", self.ARM64.value: "linux/arm64"}
        return mapping[self.value]


class ContainerFunction(pulumi.ComponentResource):
    arn: str
    name: str

    def __init__(
        self,
        name: str,
        repository: aws.ecr.Repository,
        build_and_push: bool = True,
        dockerfile: Optional[Union[str, Path]] = None,
        context: Optional[Union[str, Path]] = None,
        description: Optional[str] = None,
        memory_size: Optional[int] = 512,
        timeout: Optional[int] = 3,
        architecture: Architecture = Architecture.X86_64,
        environment: Optional[Dict[str, str]] = None,
        policy_document: Optional[str] = None,
        keep_warm: bool = False,
        use_buildx: bool = False,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__(  # type: ignore
            t="nuage:aws:ContainerFunction", name=name, props=None, opts=opts
        )

        dockerfile = Path(dockerfile or "./Dockerfile")
        context = str(dockerfile.parent) if not context else str(context)
        dockerfile = str(dockerfile)

        image_uri = repository.repository_url.apply(
            lambda uri: f"{uri}:{name}-{architecture.lambda_value}"
        )

        if build_and_push:

            if use_buildx:

                def get_buildx_registry(registry_id: str):
                    credentials = aws.ecr.get_credentials(registry_id)
                    server = credentials.proxy_endpoint
                    username, password = (
                        base64.b64decode(credentials.authorization_token)
                        .decode()
                        .split(":")
                    )
                    return buildx.RegistryArgs(
                        server=server, username=username, password=password
                    )

                image = buildx.Image(
                    resource_name=f"{name}-image",
                    name=image_uri,
                    registry=repository.registry_id.apply(get_buildx_registry),
                    platforms=[architecture.docker_value],
                    # dockerfile=dockerfile,
                    context=context,
                    opts=pulumi.ResourceOptions(parent=self),
                )

                image_uri = image.name
                # image.repo_digest
            else:

                def get_docker_registry(registry_id: str):
                    credentials = aws.ecr.get_credentials(registry_id)
                    server = credentials.proxy_endpoint
                    username, password = (
                        base64.b64decode(credentials.authorization_token)
                        .decode()
                        .split(":")
                    )
                    return docker.ImageRegistry(
                        server=server, username=username, password=password
                    )

                image = docker.Image(
                    name=name,
                    image_name=image_uri,
                    build=docker.DockerBuild(
                        dockerfile=dockerfile,
                        context=context,
                        extra_options=["--platform", architecture.docker_value],
                    ),
                    registry=repository.registry_id.apply(get_docker_registry),
                    opts=pulumi.ResourceOptions(parent=self),
                )

                image_uri = image.image_name

        role = aws.iam.Role(
            resource_name=f"{name}-lambda-role",
            name=f"{name}-lambda-role",
            description=f"Role used by {name}",
            assume_role_policy=aws.iam.get_policy_document(
                version="2012-10-17",
                statements=[
                    aws.iam.GetPolicyDocumentStatementArgs(
                        actions=["sts:AssumeRole"],
                        effect="Allow",
                        sid="",
                        principals=[
                            aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                                type="Service", identifiers=["lambda.amazonaws.com"]
                            ),
                        ],
                    ),
                ],
            ).json,
            opts=pulumi.ResourceOptions(parent=self),
        )

        combined_policy_document = aws.iam.get_policy_document(
            source_policy_documents=[
                # Can write logs to CloudWatch
                aws.iam.get_policy(name="AWSLambdaBasicExecutionRole").policy,
                # Can write Lambda Insights logs to CloudWatch
                # NB: is actually a subset of the above
                aws.iam.get_policy(
                    name="CloudWatchLambdaInsightsExecutionRolePolicy"
                ).policy,
                # Can push traces to X-Ray
                aws.iam.get_policy(name="AWSXRayDaemonWriteAccess").policy,
            ]
        ).json
        if policy_document:
            # Merge our custom policy document with the base
            combined_policy_document = aws.iam.get_policy_document(
                source_policy_documents=[
                    combined_policy_document,
                    policy_document,
                ]
            ).json

        policy = aws.iam.Policy(
            resource_name=f"{name}-lambda-policy",
            name=f"{name}-lambda-policy",
            description=f"Policy for {name}-lambda-function",
            policy=combined_policy_document,
            opts=pulumi.ResourceOptions(parent=role),
        )
        aws.iam.RolePolicyAttachment(
            resource_name=f"{name}-lambda-role-policy-attachment",
            role=role.id,
            policy_arn=policy.arn,
            opts=pulumi.ResourceOptions(parent=role),
        )

        function = aws.lambda_.Function(
            resource_name=f"{name}-lambda-function",
            name=name,
            description=description,
            package_type="Image",
            image_uri=image_uri,
            memory_size=memory_size,
            timeout=timeout,
            architectures=[architecture.lambda_value],
            role=role.arn,
            environment=aws.lambda_.FunctionEnvironmentArgs(variables=environment)
            if environment
            else None,
            tracing_config=aws.lambda_.FunctionTracingConfigArgs(mode="Active"),
            opts=pulumi.ResourceOptions(parent=self),
        )

        if keep_warm:
            rule = aws.cloudwatch.EventRule(
                resource_name=f"{name}-keep-warm-rule",
                description=f"Refreshes {name} regularly to keep the container warm",
                is_enabled=True,
                role_arn=None,
                schedule_expression="rate(5 minutes)",
                opts=pulumi.ResourceOptions(parent=function),
            )
            aws.lambda_.Permission(
                resource_name=f"{name}-cloudwatch-invoke-permission",
                action="lambda:InvokeFunction",
                function=function.arn,
                principal="events.amazonaws.com",
                source_arn=rule.arn,
                opts=pulumi.ResourceOptions(parent=rule),
            )
            aws.cloudwatch.EventTarget(
                resource_name=f"{name}-keep-warm-target",
                arn=function.arn,
                input="{}",
                rule=rule.id,
            )

        self.set_outputs({"arn": function.arn, "name": function.name})

    def set_outputs(self, outputs: Dict[str, Any]):
        """
        Adds the Pulumi outputs as attributes on the current object so they can be
        used as outputs by the caller, as well as registering them.
        """
        for output_name in outputs.keys():
            setattr(self, output_name, outputs[output_name])

        self.register_outputs(outputs)  # type: ignore
