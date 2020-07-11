from aws_cdk import (
    aws_ec2 as ec2,
    aws_dynamodb as dynamo,
    aws_lambda as _lambda,
    aws_apigateway as gateway,
    core
)

from cdk_watchful import Watchful


class HelloWorldCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        table = dynamo.Table(
            self,
            "hello-world-cdk-table",
            partition_key=dynamo.Attribute(name="id", type=dynamo.AttributeType.STRING)
        )

        function = _lambda.Function(
            self,
            "hello-world-cdk-lambda",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="handler.main",
            code=_lambda.Code.asset("./lambda")
        )

        table.grant_read_write_data(function)
        function.add_environment("TABLE_NAME", table.table_name)

        gateway.LambdaRestApi(self, "hello-world-cdk-api", handler=function)

        nat_gateway_provider = ec2.NatProvider.instance(
            instance_type=ec2.InstanceType("t3.small")
        )

        # The code that defines your stack goes here
        ec2.Vpc(
            self,
            "hello-world-cdk-vpc",
            nat_gateway_provider=nat_gateway_provider,
            nat_gateways=1
            )

        monitor = Watchful(self, "url-shortener-monitor", alarm_email="cesar.alcancio@payclip.com")
        monitor.watch_scope(self)