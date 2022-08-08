"""
Set of common variables to be uses throughout the Pulumi project
"""
from enum import Enum

import pulumi


class Environment(Enum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


ORG = "nuage"
project = pulumi.get_project()
env = pulumi.get_stack()


def is_prod() -> bool:
    return Environment(env) == Environment.PROD


aws_config = pulumi.Config("aws")
region = aws_config.require("region")

project_config = pulumi.Config(project)
domain = project_config.require("domain")
