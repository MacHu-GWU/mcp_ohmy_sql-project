# -*- coding: utf-8 -*-

import typing as T

from pydantic import Field
from ...lazy_import import sa

from ...constants import LLMTypeEnum

from ..metadata import (
    ObjectTypeEnum,
    BaseInfo,
    BaseColumnInfo,
    BaseTableInfo,
    BaseSchemaInfo,
    BaseDatabaseInfo,
)

_ = sa.ForeignKey


class ForeignKeyInfo(BaseInfo):
    """
    Ref: https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey
    """

    object_type: ObjectTypeEnum = Field(default=ObjectTypeEnum.FOREIGN_KEY)
    onupdate: T.Optional[str] = Field(default=None)
    ondelete: T.Optional[str] = Field(default=None)
    deferrable: T.Optional[bool] = Field(default=None)
    initially: T.Optional[str] = Field(default=None)


_ = sa.Column


class ColumnInfo(BaseColumnInfo):
    """
    Ref: https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column
    """

    fullname: str = Field()
    type: str = Field()
    llm_type: T.Optional[LLMTypeEnum] = Field(default=None)
    primary_key: bool = Field(default=False)
    nullable: bool = Field(default=False)
    index: T.Optional[bool] = Field(default=None)
    unique: T.Optional[bool] = Field(default=None)
    system: bool = Field(default=False)
    doc: T.Optional[str] = Field(default=None)
    autoincrement: str = Field(default="")
    constraints: list[str] = Field(default_factory=list)
    foreign_keys: list[ForeignKeyInfo] = Field(default_factory=list)
    computed: bool = Field(default=False)
    identity: bool = Field(default=False)


_ = sa.Table


class TableInfo(BaseTableInfo):
    """
    Ref: https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table
    """

    fullname: str = Field()
    primary_key: list[str] = Field(default_factory=list)
    foreign_keys: list[ForeignKeyInfo] = Field(default_factory=list)
    columns: list[ColumnInfo] = Field(default_factory=list)


class SchemaInfo(BaseSchemaInfo):
    tables: list[TableInfo] = Field(default_factory=list)


class DatabaseInfo(BaseDatabaseInfo):
    schemas: list[SchemaInfo] = Field(default_factory=list)
