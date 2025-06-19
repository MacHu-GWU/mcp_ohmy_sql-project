# -*- coding: utf-8 -*-

"""
In Python, we can use Pydantic to define a tagged union
(also known as a discriminated union) using the `discriminator` field.
This allows us to create a union type that can be used to represent
different subtypes of a base type, where each subtype has its own specific fields.
"""

import typing as T
from pydantic import BaseModel, Field


class BaseConnection(BaseModel):
    type: str = Field()


class SqlalchemyConnection(BaseConnection):
    type: T.Literal["sqlalchemy"] = Field(default="sqlalchemy")
    create_engine_kwargs: dict[str, T.Any] = Field(default_factory=dict)


class AwsConnection(BaseConnection):
    type: T.Literal["aws"] = Field(default="aws")
    boto_session_kwargs: dict[str, T.Any] = Field(default_factory=dict)


class Config(BaseModel):
    connection: T.Union[SqlalchemyConnection, AwsConnection] = Field(
        discriminator="type"
    )


if __name__ == "__main__":
    dct_sql = {"connection": {"type": "sqlalchemy", "create_engine_kwargs": {}}}
    dct_aws = {"connection": {"type": "aws", "boto_session_kwargs": {}}}

    config = Config(**dct_sql)
    # config = Config(**dct_aws)

    print(config)
