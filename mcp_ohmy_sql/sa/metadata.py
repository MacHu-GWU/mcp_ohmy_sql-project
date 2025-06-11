# -*- coding: utf-8 -*-

import typing as T
from functools import cached_property

import sqlalchemy as sa

from pydantic import BaseModel, Field

from ..constants import TableTypeEnum
from ..utils import match

from .types import ColumnType

try:  # pragma: no cover
    from rich import print as rprint
except ImportError:  # pragma: no cover
    pass


class ForeignKeyInfo(BaseModel):
    object_type: str = Field(default="foreign key")
    name: str = Field()
    comment: T.Optional[str] = Field(default=None)
    onupdate: T.Optional[str] = Field(default=None)
    ondelete: T.Optional[str] = Field(default=None)
    deferrable: T.Optional[bool] = Field(default=None)
    initially: T.Optional[str] = Field(default=None)

    @classmethod
    def from_foreign_key(
        cls,
        fk: sa.ForeignKey,
    ):
        return cls(
            name=str(fk.column),
            comment=fk.comment,
            onupdate=fk.onupdate,
            ondelete=fk.ondelete,
            deferrable=fk.deferrable,
            initially=fk.initially,
        )


class ColumnInfo(BaseModel):
    object_type: str = Field(default="column")
    name: str = Field()
    fullname: str = Field()
    type: "ColumnType" = Field()
    nullable: bool = Field(default=False)
    index: T.Optional[bool] = Field(default=None)
    unique: T.Optional[bool] = Field(default=None)
    system: bool = Field(default=False)
    doc: T.Optional[str] = Field(default=None)
    comment: T.Optional[str] = Field(default=None)
    autoincrement: str = Field(default="")
    constraints: list[str] = Field(default_factory=list)
    foreign_keys: list[ForeignKeyInfo] = Field(default_factory=list)
    computed: bool = Field(default=False)
    identity: bool = Field(default=False)

    @classmethod
    def from_column(
        cls,
        table: sa.Table,
        column: sa.Column,
    ):
        foreign_keys = list()
        for fk in column.foreign_keys:
            fk_info = ForeignKeyInfo.from_foreign_key(fk)
            # rprint(fk_info.model_dump())  # for debug only
            foreign_keys.append(fk_info)

        return ColumnInfo(
            name=column.name,
            fullname=f"{table.name}.{column.name}",
            type=ColumnType.from_type(column.type),
            nullable=column.nullable,
            index=column.index,
            unique=column.unique,
            system=column.system,
            doc=column.doc,
            comment=column.comment,
            autoincrement=str(column.autoincrement),
            constraints=[str(c) for c in column.constraints],
            foreign_keys=foreign_keys,
            computed=bool(column.computed),
            identity=bool(column.identity),
        )


class TableInfo(BaseModel):
    object_type: str = Field()
    name: str = Field()
    fullname: str = Field()
    comment: T.Optional[str] = Field(default=None)
    primary_key: list[str] = Field(default_factory=list)
    foreign_keys: list[ForeignKeyInfo] = Field(default_factory=list)
    columns: list[ColumnInfo] = Field(default_factory=list)

    @cached_property
    def columns_mapping(self) -> dict[str, ColumnInfo]:
        """
        Returns a mapping of column names to ColumnInfo objects for easy access.
        """
        return {column.name: column for column in self.columns}

    @classmethod
    def from_table(
        cls,
        table: sa.Table,
        object_type: str,
    ):
        foreign_keys = list()
        for fk in table.foreign_keys:
            fk_info = ForeignKeyInfo.from_foreign_key(fk)
            # rprint(fk_info.model_dump())  # for debug only
            foreign_keys.append(fk_info)

        columns = list()
        for _, column in table.columns.items():
            column_info = ColumnInfo.from_column(table, column)
            # rprint(column_info.model_dump())  # for debug only
            columns.append(column_info)

        return TableInfo(
            object_type=object_type,
            name=table.name,
            comment=table.comment,
            fullname=table.fullname,
            primary_key=[col.name for col in table.primary_key.columns],
            foreign_keys=foreign_keys,
            columns=columns,
        )


class SchemaInfo(BaseModel):
    object_type: str = Field(default="schema")
    name: str = Field(default="")
    comment: T.Optional[str] = Field(default=None)
    tables: list[TableInfo] = Field(default_factory=list)

    @cached_property
    def tables_mapping(self) -> dict[str, TableInfo]:
        """
        Returns a mapping of table names to TableInfo objects for easy access.
        """
        return {table.name: table for table in self.tables}

    @classmethod
    def from_metadata(
        cls,
        engine: sa.engine.Engine,
        metadata: sa.MetaData,
        schema_name: T.Optional[str],
        include: T.Optional[list[str]] = None,
        exclude: T.Optional[list[str]] = None,
    ):
        """
        :param engine: SQLAlchemy engine
        :param metadata: we assume metadata is already reflected
        """
        insp = sa.inspect(engine)
        try:
            view_names = set(insp.get_view_names(schema=schema_name))
        except NotImplementedError:  # pragma: no cover
            view_names = set()
        try:
            materialized_view_names = set(insp.get_materialized_view_names())
        except NotImplementedError:  # pragma: no cover
            materialized_view_names = set()

        if include is None:  # pragma: no cover
            include = []
        if exclude is None:  # pragma: no cover
            exclude = []

        tables = list()
        for table_name, table in metadata.tables.items():
            # don't include tables from other schemas
            if table.schema != schema_name:  # pragma: no cover
                continue
            # don't include tables that don't match the criteria
            if match(table_name, include, exclude) is False:
                continue

            if table_name in view_names:  # pragma: no cover
                object_type = TableTypeEnum.VIEW.value
            elif table_name in materialized_view_names:  # pragma: no cover
                object_type = TableTypeEnum.MATERIALIZED_VIEW.value
            else:
                object_type = TableTypeEnum.TABLE.value
            table_info = TableInfo.from_table(table=table, object_type=object_type)
            # rprint(table_info.model_dump()) # for debug only
            tables.append(table_info)

        return SchemaInfo(
            name=metadata.schema or "",
            tables=tables,
        )
