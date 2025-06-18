# -*- coding: utf-8 -*-

"""
Base connection configuration classes for database connections.
"""

from pydantic import BaseModel, Field, field_validator

from ..constants import ConnectionTypeEnum


class BaseConnection(BaseModel):
    """
    Base class for database connection configurations.
    """

    type: str = Field()

    @field_validator("type", mode="after")
    @classmethod
    def check_type(cls, value: str) -> str:  # pragma: no cover
        """
        Validate the type field.
        """
        if ConnectionTypeEnum.is_valid_value(value) is False:
            raise ValueError(f"{value} is not a valid value of {ConnectionTypeEnum}")
        return value
