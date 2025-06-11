# -*- coding: utf-8 -*-

"""
This module provides an enumeration of pre-configured Boto Session Manager
instances for different AWS environments and accounts.
"""

from functools import cached_property
from boto_session_manager import BotoSesManager
from which_runtime.api import runtime


class BsmEnum:
    """
    Use lazy loading to create enum values.
    """

    def _get_bsm(self, profile: str) -> BotoSesManager:
        if runtime.is_ci_runtime_group:
            return BotoSesManager(region_name="us-east-1")
        else:
            return BotoSesManager(profile_name=profile)

    @cached_property
    def dev(self):
        return self._get_bsm("esc_app_dev_us_east_1")


bsm_enum = BsmEnum()
