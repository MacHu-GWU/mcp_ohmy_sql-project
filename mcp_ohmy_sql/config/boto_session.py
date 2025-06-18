# -*- coding: utf-8 -*-

"""
AWS Boto3 session configuration for database connections.
"""

import typing as T

from pydantic import BaseModel, Field

from ..lazy_import import BotoSesManager


class BotoSessionKwargs(BaseModel):
    """
    AWS credentials and session configuration for Boto3 clients.

    .. tip::

        See `boto_session_manager <https://github.com/MacHu-GWU/boto_session_manager-project>`_
        official documentation for more details on how to use this class.
    """
    aws_access_key_id: T.Optional[str] = Field(default=None)
    aws_secret_access_key: T.Optional[str] = Field(default=None)
    aws_session_token: T.Optional[str] = Field(default=None)
    region_name: T.Optional[str] = Field(default=None)
    profile_name: T.Optional[str] = Field(default=None)
    role_arn: T.Optional[str] = Field(default=None)
    duration_seconds: int = Field(default=3600)
    auto_refresh: bool = Field(default=False)

    def get_bsm(self) -> "BotoSesManager":
        """
        Get a configured BotoSesManager instance.
        """
        kwargs = dict(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_session_token=self.aws_session_token,
            region_name=self.region_name,
            profile_name=self.profile_name,
        )
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        bsm = BotoSesManager(**kwargs)
        # If role_arn is provided, assume the role
        if isinstance(self.role_arn, str):
            bsm = bsm.assume_role(
                role_arn=self.role_arn,
                duration_seconds=self.duration_seconds,
                auto_refresh=self.auto_refresh,
            )
        return bsm
