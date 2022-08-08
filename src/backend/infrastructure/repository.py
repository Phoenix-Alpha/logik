import base64
import json

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker

from .common import env, project

repository = aws.ecr.Repository(
    resource_name=f"{project}-repository",
    name=f"{project}-{env}",
)

pulumi.export("repository_url", repository.repository_url)

aws.ecr.LifecyclePolicy(
    resource_name=f"{project}-lifecycle-policy",
    repository=repository.id,
    policy=json.dumps(
        {
            "rules": [
                {
                    "rulePriority": 1,
                    "description": "Keep only one untagged image, expire all others",
                    "selection": {
                        "tagStatus": "untagged",
                        "countType": "imageCountMoreThan",
                        "countNumber": 1,
                    },
                    "action": {
                        "type": "expire",
                    },
                }
            ]
        }
    ),
    opts=pulumi.ResourceOptions(parent=repository),
)


def getRegistryInfo(registry_id):
    """
    Get registry info (credentials and endpoint)
    https://www.pulumi.com/blog/build-publish-containers-iac/#authenticate-with-temporary-ecr-access-token
    """
    creds = aws.ecr.get_credentials(registry_id=registry_id)
    decoded = base64.b64decode(creds.authorization_token).decode()
    parts = decoded.split(":")
    if len(parts) != 2:
        raise Exception("Invalid credentials")
    return docker.ImageRegistry(creds.proxy_endpoint, parts[0], parts[1])
