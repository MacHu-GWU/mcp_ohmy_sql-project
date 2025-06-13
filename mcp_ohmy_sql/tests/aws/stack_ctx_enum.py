# -*- coding: utf-8 -*-

"""
This module provides an enumeration of pre-configured cloudformation stack
context information for different stacks.
"""

from functools import cached_property

from cdk_mate.api import StackCtx

from .constants import stack_name
from .bsm_enum import bsm_enum


class StackCtxEnum:
    """
    Use lazy loading to create enum values.
    """

    @cached_property
    def my_ohmy_sql_dev(self):
        return StackCtx.new(
            stack_name=stack_name,
            bsm=bsm_enum.dev,
        )


stack_ctx_enum = StackCtxEnum()
