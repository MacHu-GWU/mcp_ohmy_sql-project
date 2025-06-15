# -*- coding: utf-8 -*-

import typing as T

from pydantic import Field

from ...constants import LLMTypeEnum

from ..metadata import (
    BaseColumnInfo,
    BaseTableInfo,
    BaseSchemaInfo,
    BaseDatabaseInfo,
)


class ColumnInfo(BaseColumnInfo):

    fullname: str = Field()
    type: str = Field()
    llm_type: T.Optional[LLMTypeEnum] = Field(default=None)
    dist_key: bool = Field(default=False)
    sort_key: bool = Field(default=False)
    sort_key_order: int = Field(default=0)
    unique: T.Optional[bool] = Field(default=None)
    foreign_keys: T.Optional[str] = Field(default=None)


class TableInfo(BaseTableInfo):
    fullname: str = Field()
    dist_key_type: str = Field()
    columns: list[ColumnInfo] = Field(default_factory=list)


class SchemaInfo(BaseSchemaInfo):
    tables: list[TableInfo] = Field(default_factory=list)


class DatabaseInfo(BaseDatabaseInfo):
    schemas: list[SchemaInfo] = Field(default_factory=list)
