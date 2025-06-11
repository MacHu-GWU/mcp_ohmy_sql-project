# -*- coding: utf-8 -*-

"""
Stack Initialization for Multi-Account AWS CDK Deployment
"""

import dataclasses
from functools import cached_property

import aws_cdk as cdk

from .stacks.mcp_ohmy_sql_stack.iac_define import Stack

from .stack_ctx_enum import stack_ctx_enum


@dataclasses.dataclass
class StackEnum:
    """
    Enumeration of CDK stacks for different environments.
    """

    app: cdk.App = dataclasses.field()

    @cached_property
    def my_ohmy_sql_dev(self):
        return Stack(
            scope=self.app,
            **stack_ctx_enum.my_ohmy_sql_dev.to_stack_kwargs(),
        )


# Create the global stack enumeration instance
app = cdk.App()

stack_enum = StackEnum(app=app)
