import pulumi
import pulumi_aws as aws
import yaml

from ..common import ORG, Environment, domain, env, is_prod, project

zone = aws.route53.Zone(
    resource_name="zone",
    name=domain,
    comment=f"DNS records for {project} ({env})",
    opts=pulumi.ResourceOptions(protect=is_prod()),
)
pulumi.export("zone_id", zone.id)

if not is_prod():
    # If we're not on the production stack, then the main DNS zone is held by it so
    # we need to get the `zone_id` using a stack reference, then create our NS records
    # to link the prod zone to the other DNS zones

    prod_stack = pulumi.StackReference(
        name=f"{ORG}/{project}/{Environment.PROD.value}",
        opts=pulumi.ResourceOptions(parent=zone),
    )
    zone_id = prod_stack.require_output("zone_id")

    with open(f"infrastructure/stacks/Pulumi.{Environment.PROD.value}.yaml") as f:
        prod_config = yaml.safe_load(f)["config"]

    prod_provider = aws.provider.Provider(
        resource_name=f"aws-provider-{Environment.PROD.value}",
        region=prod_config["aws:region"],
        profile=prod_config["aws:profile"],
        allowed_account_ids=prod_config["aws:allowedAccountIds"],
        default_tags=prod_config["aws:defaultTags"],
        opts=pulumi.ResourceOptions(parent=prod_stack),
    )

    name_server_record = aws.route53.Record(
        resource_name=f"record-NS-{env}",
        name=domain,
        type="NS",
        ttl=300,
        records=zone.name_servers,
        zone_id=zone_id,
        opts=pulumi.ResourceOptions(provider=prod_provider, parent=prod_provider),
    )
