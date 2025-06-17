# -*- coding: utf-8 -*-

import typing as T

from pydantic import Field

from ...constants import DbTypeEnum, LLMTypeEnum

from ..metadata import (
    BaseColumnInfo,
    BaseTableInfo,
    BaseSchemaInfo,
    BaseDatabaseInfo,
)


class ColumnInfo(BaseColumnInfo):
    name: str = Field()
    type: str = Field()
    llm_type: T.Optional[LLMTypeEnum] = Field(default=None)
    dist_key: bool = Field(default=False)
    sort_key_position: int = Field()
    encoding: T.Optional[str] = Field(default=None)
    notnull: T.Optional[bool] = Field(default=None)


class TableInfo(BaseTableInfo):
    name: str = Field()
    dist_style: str = Field()
    owner: str = Field()
    columns: list[ColumnInfo] = Field(default_factory=list)


class SchemaInfo(BaseSchemaInfo):
    tables: list[TableInfo] = Field(default_factory=list)


class DatabaseInfo(BaseDatabaseInfo):
    db_type: DbTypeEnum = Field(default=DbTypeEnum.AWS_REDSHIFT)
    schemas: list[SchemaInfo] = Field(default_factory=list)
