import pulumi
from pulumi_aws import acm, route53

from ..common import domain, env
from .zone import zone

certificate = acm.Certificate(
    resource_name=f"certificate-{env}",
    domain_name=domain,
    subject_alternative_names=[f"*.{domain}"],
    validation_method="DNS",
)

# SSL certificate verification

validation_records = certificate.domain_validation_options.apply(
    lambda dvos: [
        route53.Record(
            resource_name=f"record-certificate-validation-{i+1}",
            name=dvo["resource_record_name"],
            records=[dvo["resource_record_value"]],
            type=dvo["resource_record_type"],
            ttl=300,
            zone_id=zone.id,
            # APEX & wildcard share the same validation record,
            # so we need to allow overwrite to avoid duplicates
            allow_overwrite=True,
            opts=pulumi.ResourceOptions(parent=certificate),
        )
        for i, dvo in enumerate(dvos)
    ]
)

certificate_validation = acm.CertificateValidation(
    resource_name="certificate-validation",
    certificate_arn=certificate.arn,
    validation_record_fqdns=validation_records.apply(
        lambda records: [record.fqdn for record in records]
    ),
    opts=pulumi.ResourceOptions(parent=certificate),
)
