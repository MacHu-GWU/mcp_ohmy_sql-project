# -*- coding: utf-8 -*-

import aws_cdk as cdk
from constructs import Construct


class Stack(
    cdk.Stack,
):
    def __init__(
        self,
        scope: Construct,
        id: str,
        stack_name: str,
        env: cdk.Environment,
    ):
        super().__init__(
            scope=scope,
            id=id,
            stack_name=stack_name,
            env=env,
        )
