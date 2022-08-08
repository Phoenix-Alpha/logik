from typing import Any, Dict, Optional

import pulumi
import pulumi_aws as aws

from .container_function import ContainerFunction


class ServerlessApi(pulumi.ComponentResource):
    endpoint: str

    def __init__(
        self,
        name: str,
        function: ContainerFunction,
        description: Optional[str] = None,
        cors_configuration: Optional[aws.apigatewayv2.ApiCorsConfigurationArgs] = None,
        domain_name: Optional[str] = None,
        certificate_validation: Optional[aws.acm.CertificateValidation] = None,
        zone: Optional[aws.route53.Zone] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        """
        :name: prefix being used for every resource created in this component
        :function: the Lambda function that contains the code for this API
        :description: description of the API
        :cors_configuration: domains that are whitelisted for cross-site requests
        :domain_name: optional domain name on which to host the API
        :certificate_validation: we need a validated SSL certificate in order to use
            a custom domain name
        :zone: the DNS zone on which records will be created
        """
        super().__init__(t="nuage:aws:ServerlessApi", name=name, props=None, opts=opts)

        api = aws.apigatewayv2.Api(
            resource_name=f"{name}-API",
            name=f"{name}-API",
            protocol_type="HTTP",
            description=description,
            route_key="$default",
            target=function.arn,
            cors_configuration=cors_configuration,
            opts=pulumi.ResourceOptions(parent=self),
        )

        aws.lambda_.Permission(
            resource_name=f"{name}-lambda-invoke-permission",
            action="lambda:InvokeFunction",
            function=function.arn,
            principal="apigateway.amazonaws.com",
            source_arn=pulumi.Output.all(api.execution_arn, api.route_key).apply(
                lambda values: f"{values[0]}/*/{values[1]}"
            ),
            opts=pulumi.ResourceOptions(parent=api),
        )

        outputs = {"endpoint": api.api_endpoint}

        if domain_name and zone and certificate_validation:
            api_domain_name = aws.apigatewayv2.DomainName(
                resource_name=f"{name}-domain-name",
                domain_name=domain_name,
                domain_name_configuration=aws.apigatewayv2.DomainNameDomainNameConfigurationArgs(  # noqa
                    certificate_arn=certificate_validation.certificate_arn,
                    endpoint_type="REGIONAL",
                    security_policy="TLS_1_2",
                ),
                # NB: this resource requires that the certificate be validated in order
                # to deploy
                opts=pulumi.ResourceOptions(
                    parent=self, depends_on=[certificate_validation]
                ),
            )

            aws.apigatewayv2.ApiMapping(
                resource_name=f"{name}-api-mapping",
                domain_name=api_domain_name.id,
                api_id=api.id,
                stage="$default",
                opts=pulumi.ResourceOptions(parent=self),
            )

            # API DNS record
            is_apex = zone.name.apply(lambda name: bool(name == domain_name))
            if not is_apex:
                # CNAME record
                aws.route53.Record(
                    resource_name=f"{name}-api-record",
                    name=zone.name,
                    records=[
                        api_domain_name.domain_name_configuration.target_domain_name
                    ],
                    type="CNAME",
                    ttl=300,
                    zone_id=zone.id,
                    opts=pulumi.ResourceOptions(parent=self),
                )
            else:
                # Alias record
                aws.route53.Record(
                    resource_name=f"{name}-api-record",
                    aliases=[
                        aws.route53.RecordAliasArgs(
                            name=api_domain_name.domain_name_configuration.target_domain_name,  # noqa
                            zone_id=api_domain_name.domain_name_configuration.hosted_zone_id,  # noqa
                            evaluate_target_health=True,
                        )
                    ],
                    name=domain_name,
                    type="A",
                    zone_id=zone.id,
                    opts=pulumi.ResourceOptions(parent=self),
                )

            outputs["endpoint"] = api_domain_name.domain_name.apply(
                lambda domain: f"https://{domain}"
            )

        self.set_outputs(outputs)

    def set_outputs(self, outputs: Dict[str, Any]):
        """
        Adds the Pulumi outputs as attributes on the current object so they can be
        used as outputs by the caller, as well as registering them.
        """
        for output_name in outputs.keys():
            setattr(self, output_name, outputs[output_name])

        self.register_outputs(outputs)  # type: ignore
