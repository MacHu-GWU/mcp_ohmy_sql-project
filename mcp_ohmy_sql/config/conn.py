# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field, field_validator

from ..constants import ConnectionTypeEnum


class BaseConnection(BaseModel):
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
