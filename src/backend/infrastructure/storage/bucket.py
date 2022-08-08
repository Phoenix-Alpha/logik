import pulumi_aws as aws

from ..common import env, project, region

transfer_bucket = aws.s3.Bucket(
    resource_name="storage-manager-bucket",
    bucket=f"{project}-storage-manager-{env}-{region}",
    acl="private",
)
