import pulumi
import pulumi_aws as aws

from ..common import env, project
from ..components.container_function import Architecture, ContainerFunction
from ..dns.zone import zone
from ..repository import repository
from .bucket import transfer_bucket

transfer_assume_role_policy = aws.iam.get_policy_document(
    statements=[
        aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            actions=["sts:AssumeRole"],
            principals=[
                aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    type="Service", identifiers=["transfer.amazonaws.com"]
                )
            ],
        )
    ],
)

transfer_access_role = aws.iam.Role(
    resource_name="ftp-auth-function-role",
    name=f"{project}-ftp-auth-function-role-{env}",
    description=(
        "IAM role used by Transfer to give access to S3 bucket after user is"
        " authenticated"
    ),
    assume_role_policy=transfer_assume_role_policy.json,
)

transfer_access_policy = aws.iam.RolePolicy(
    resource_name="ftp-auth-function-policy",
    name=f"{project}-ftp-auth-function-policy-{env}",
    role=transfer_access_role.name,
    policy=aws.iam.get_policy_document(
        statements=[
            aws.iam.GetPolicyDocumentStatementArgs(
                effect="Allow",
                actions=["s3:ListBucket"],
                resources=[transfer_bucket.arn],  # type: ignore
            ),
            aws.iam.GetPolicyDocumentStatementArgs(
                effect="Allow",
                actions=[
                    "s3:PutObject",
                    "s3:PutObjectAcl",
                    "s3:GetObject",
                    "s3:GetObjectAcl",
                    "s3:GetObjectVersion",
                    "s3:DeleteObject",
                    "s3:DeleteObjectVersion",
                    "s3:GetBucketLocation",
                ],
                resources=[
                    transfer_bucket.arn,  # type: ignore
                    transfer_bucket.arn.apply(lambda arn: f"{arn}/*"),
                ],
            ),
        ],
    ).json,
)

auth_function = ContainerFunction(
    name=f"{project}-ftp-auth-function-{env}",
    description=(
        "Function that manages the authentication between the AWS Transfer FTP server"
        " and the GraphQL API"
    ),
    architecture=Architecture.ARM64,
    repository=repository,
    dockerfile="infrastructure/storage/auth_function/Dockerfile",
    use_buildx=False,
    environment={  # type: ignore
        "POWERTOOLS_SERVICE_NAME": f"{project}-ftp-auth",
        "TRANSFER_ACCESS_ROLE_ARN": transfer_access_role.arn,
        "TRANSFER_BUCKET_NAME": transfer_bucket.bucket,
    },
)

# AWS Transfer FTP server

transfer_service_role = aws.iam.Role(
    resource_name="transfer-service-role",
    name=f"AWSTransferLoggingAccess-{env}",
    assume_role_policy=transfer_assume_role_policy.json,
    path="/service-role/",
)

ftp_server = aws.transfer.Server(
    resource_name="ftp-server",
    domain="S3",
    endpoint_type="PUBLIC",
    force_destroy=False,
    function=auth_function.arn,
    identity_provider_type="AWS_LAMBDA",
    logging_role=transfer_service_role.arn,
    security_policy_name="TransferSecurityPolicy-2020-06",
)

aws.lambda_.Permission(
    resource_name="transfer-invoke-permission",
    action="lambda:InvokeFunction",
    function=auth_function.arn,
    principal="transfer.amazonaws.com",
    source_arn=ftp_server.arn,
    opts=pulumi.ResourceOptions(parent=auth_function),
)

aws.route53.Record(
    resource_name="ftp-record",
    name=zone.name.apply(lambda domain: f"storage.{domain}"),
    records=[ftp_server.endpoint],
    type="CNAME",
    ttl=300,
    zone_id=zone.id,
    opts=pulumi.ResourceOptions(parent=ftp_server),
)
