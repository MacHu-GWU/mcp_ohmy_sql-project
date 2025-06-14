# -*- coding: utf-8 -*-

import typing as T
from functools import cached_property

from pydantic import BaseModel, Field

from ..constants import ObjectTypeEnum, DbTypeEnum


class BaseInfo(BaseModel):
    object_type: ObjectTypeEnum = Field()
    name: str = Field()
    comment: T.Optional[str] = Field(default=None)


class BaseColumnInfo(BaseInfo):
    object_type: ObjectTypeEnum = Field(default=ObjectTypeEnum.COLUMN)


class BaseTableInfo(BaseInfo):
    columns: list[BaseColumnInfo] = Field(default_factory=list)

    @cached_property
    def columns_mapping(self) -> dict[str, BaseColumnInfo]:
        """
        Returns a mapping of column names to BaseColumnInfo objects for easy access.
        """
        return {column.name: column for column in self.columns}


class BaseSchemaInfo(BaseInfo):
    object_type: ObjectTypeEnum = Field(default=ObjectTypeEnum.SCHEMA)
    tables: list[BaseTableInfo] = Field(default_factory=list)

    @cached_property
    def tables_mapping(self) -> dict[str, BaseTableInfo]:
        """
        Returns a mapping of table names to BaseTableInfo objects for easy access.
        """
        return {table.name: table for table in self.tables}


class BaseDatabaseInfo(BaseInfo):
    object_type: ObjectTypeEnum = Field(default=ObjectTypeEnum.DATABASE)
    db_type: DbTypeEnum = Field()
    schemas: list[BaseSchemaInfo] = Field(default_factory=list)

    @cached_property
    def schemas_mapping(self) -> dict[str, BaseSchemaInfo]:
        """
        Returns a mapping of schema names to BaseSchemaInfo objects for easy access.
        """
        return {schema.name: schema for schema in self.schemas}
