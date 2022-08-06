import os
import aws_cdk as cdk
import aws_cdk.aws_ec2 as _ec2
from aws_cdk import aws_sagemaker as _sagemaker


class SagemakerMigrationStack(cdk.Stack):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC with private subnet and S3 endpoint (Gateway endpoint)
        sagemaker_vpc = _ec2.Vpc(self, 'sagemaker-vpc',
                                 vpc_name='sagemaker-vpc',
                                 cidr='10.0.0.0/16',
                                 nat_gateways=0,
                                 max_azs=1,
                                 enable_dns_hostnames=True,
                                 enable_dns_support=True,
                                 subnet_configuration=[_ec2.SubnetConfiguration(cidr_mask=24,
                                                                                name='sagemaker-private-subnet',
                                                                                subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED)],
                                 gateway_endpoints={'S3': _ec2.GatewayVpcEndpointOptions(
                                     service=_ec2.GatewayVpcEndpointAwsService.S3)})

        # Create Sagemaker endpoints
        _ec2.InterfaceVpcEndpoint(self, 'sagemaker-endpoint-sm-api',
                                                 vpc=sagemaker_vpc,
                                                 private_dns_enabled=True,
                                                 service=_ec2.InterfaceVpcEndpointService(
                                                     'com.amazonaws.eu-central-1.sagemaker.api',
                                                     443))

        _ec2.InterfaceVpcEndpoint(self, 'sagemaker-endpoint-sm-runtime',
                                                     vpc=sagemaker_vpc,
                                                     private_dns_enabled=True,
                                                     service=_ec2.InterfaceVpcEndpointService(
                                                         'com.amazonaws.eu-central-1.sagemaker.runtime',
                                                         443))

        _ec2.InterfaceVpcEndpoint(self, 'sagemaker-endpoint-servicecatalog',
                                                            vpc=sagemaker_vpc,
                                                            private_dns_enabled=True,
                                                            service=_ec2.InterfaceVpcEndpointService(
                                                                'com.amazonaws.eu-central-1.servicecatalog',
                                                                443))

        _ec2.InterfaceVpcEndpoint(self, 'sagemaker-endpoint-codecommit',
                                                        vpc=sagemaker_vpc,
                                                        private_dns_enabled=True,
                                                        service=_ec2.InterfaceVpcEndpointService(
                                                            'com.amazonaws.eu-central-1.git-codecommit',
                                                            443))

        _ec2.InterfaceVpcEndpoint(self, 'sagemaker-endpoint-ecr',
                                                 vpc=sagemaker_vpc,
                                                 private_dns_enabled=True,
                                                 service=_ec2.InterfaceVpcEndpointService(
                                                     'com.amazonaws.eu-central-1.ecr.dkr',
                                                     443))
