# -*- coding: utf-8 -*-

"""
Tagged Union / Discriminated Union

据中包含一个 “tag” 字段（如你的 type），用来标识这是哪一种子类型；基于该值，选择对应的模型结构解析。
Pydantic 建议也推荐使用这种方式来定义 union 类型 。
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
