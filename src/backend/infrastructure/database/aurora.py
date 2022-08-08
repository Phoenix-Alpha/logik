import pulumi

# import pulumi_aws as aws
import pulumi_random

# https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Limits.html#RDS_Limits.Constraints'
aurora_master_password = pulumi_random.RandomPassword(  # type: ignore
    resource_name="db-password",
    length=20,
    special=True,
    override_special="!#$%&*()-_=+[]<>:?",
)
pulumi.export("aurora_master_password", aurora_master_password.result)

# aurora_cluster = aws.rds.Cluster(
#     resource_name="cluster",
#     availability_zones=["eu-west-1a", "eu-west-1b", "eu-west-1c"],
#     backup_retention_period=5,
#     database_name="users",
#     engine="aurora-mysql",
#     engine_mode="serverless",
#     enable_http_endpoint=True,
#     scaling_configuration={
#         "auto_pause": True,
#         "max_capacity": 4,
#         "min_capacity": 1,
#         "seconds_until_auto_pause": 300,
#         "timeout_action": "RollbackCapacityChange",
#     },
#     port=3306,  # Config requirement for aurora serverless
#     master_password=aurora_master_password.result,
#     master_username="aurora_username",
#     preferred_backup_window="02:00-03:00",
#     db_subnet_group_name=db_subnet_group.name,
#     vpc_security_group_ids=[security_group.id],
# )
