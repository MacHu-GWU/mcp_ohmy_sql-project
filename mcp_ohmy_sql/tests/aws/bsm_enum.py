# -*- coding: utf-8 -*-

"""
This module provides an enumeration of pre-configured Boto Session Manager
instances for different AWS environments and accounts.
"""

from functools import cached_property
from boto_session_manager import BotoSesManager
from which_runtime.api import runtime

from .constants import aws_region, aws_profile


class _BsmEnum:
    """
    Use lazy loading to create enum values.
    """

    def _get_bsm(self, profile: str) -> BotoSesManager:
        if runtime.is_ci_runtime_group:
            return BotoSesManager(region_name=aws_region)
        else:
            return BotoSesManager(profile_name=profile, region_name=aws_region)

    @cached_property
    def dev(self):
        return self._get_bsm(aws_profile)


BsmEnum = _BsmEnum()
