#!/usr/bin/env python3

from aws_cdk import (
    aws_ec2 as ec2,
    core
)

from hello_world_cdk.hello_world_cdk_stack import HelloWorldCdkStack


app = core.App()
alcancioAccount = "519501257528"
payClipExternalAccount = "381734387592"
HelloWorldCdkStack(app, "hello-world-cdk", env=core.Environment(region="us-west-2", account=payClipExternalAccount))

app.synth()
