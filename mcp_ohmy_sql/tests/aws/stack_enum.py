# -*- coding: utf-8 -*-

"""
Stack Initialization for Multi-Account AWS CDK Deployment
"""

import dataclasses
from functools import cached_property

import aws_cdk as cdk

from .constants import (
    redshift_security_group_name,
    redshift_iam_role_name,
    namespace_name,
    workgroup_name,
    database_name,
)
from .stack_ctx_enum import stack_ctx_enum
from .stacks.mcp_ohmy_sql_stack.iac_define import Stack


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
            vpc_id="vpc-0d87d639dc2503350",
            security_group_name=redshift_security_group_name,
            iam_role_name=redshift_iam_role_name,
            namespace_name=namespace_name,
            db_name=database_name,
            workgroup_name=workgroup_name,
        )


# Create the global stack enumeration instance
app = cdk.App()

stack_enum = StackEnum(app=app)
