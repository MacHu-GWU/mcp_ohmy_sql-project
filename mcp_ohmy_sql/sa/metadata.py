# -*- coding: utf-8 -*-

import typing as T
import sqlalchemy as sa

from pydantic import BaseModel, Field

try:  # pragma: no cover
    from rich import print as rprint
except ImportError:  # pragma: no cover
    pass


class ForeignKeyInfo(BaseModel):
    object_type: str = Field(default="foreign key")
    name: str = Field()
    comment: str = Field(default="")
    onupdate: T.Optional[str] = Field(default=None)
    ondelete: T.Optional[str] = Field(default=None)
    deferrable: T.Optional[bool] = Field(default=None)
    initially: T.Optional[str] = Field(default=None)


def get_foreign_keys_info(
    fk: sa.ForeignKey,
) -> ForeignKeyInfo:
    return ForeignKeyInfo(
        name=fk.column.name,
        comment=fk.comment or "",
        onupdate=fk.onupdate or "",
        ondelete=fk.ondelete or "",
        deferrable=fk.deferrable,
        initially=fk.initially or "",
    )


class ColumnInfo(BaseModel):
    object_type: str = Field(default="column")
    name: str = Field()
    fullname: str = Field()
    type: str = Field()
    nullable: bool = Field(default=False)
    index: T.Optional[bool] = Field(default=False)
    unique: T.Optional[bool] = Field(default=False)
    system: bool = Field(default=False)
    doc: str = Field(default="")
    comment: str = Field(default="")
    autoincrement: str = Field(default=False)
    constraints: list[str] = Field(default_factory=list)
    foreign_keys: list[ForeignKeyInfo] = Field(default_factory=list)
    computed: bool = Field(default=False)
    identity: bool = Field(default=False)


def get_column_info(table: sa.Table, column: sa.Column):
    foreign_keys = list()
    for fk in table.foreign_keys:
        fk_info = get_foreign_keys_info(fk)
        # rprint(fk_info.model_dump())  # for debug only
        foreign_keys.append(fk_info)

    return ColumnInfo(
        name=column.name,
        fullname=f"{table.name}.{column.name}",
        type=str(column.type),
        nullable=column.nullable,
        index=column.index,
        unique=column.unique,
        system=column.system,
        doc=column.doc or "",
        comment=column.comment or "",
        autoincrement=str(column.autoincrement),
        constraints=[str(c) for c in column.constraints],
        foreign_keys=foreign_keys,
        computed=bool(column.computed),
        identity=bool(column.identity),
    )


class TableInfo(BaseModel):
    object_type: str = Field(default="table")
    name: str = Field()
    fullname: str = Field()
    primary_key: list[str] = Field(default_factory=list)
    foreign_keys: list[ForeignKeyInfo] = Field(default_factory=list)
    columns: list[ColumnInfo] = Field(default_factory=list)


def get_table_info(table: sa.Table):
    foreign_keys = list()
    for fk in table.foreign_keys:
        fk_info = get_foreign_keys_info(fk)
        # rprint(fk_info.model_dump())  # for debug only
        foreign_keys.append(fk_info)

    columns = list()
    for _, column in table.columns.items():
        column_info = get_column_info(table, column)
        # rprint(column_info.model_dump())  # for debug only
        columns.append(column_info)

    return TableInfo(
        name=table.name,
        fullname=table.fullname,
        primary_key=[str(pk) for pk in table.primary_key.columns],
        foreign_keys=foreign_keys,
        columns=columns,
    )


class SchemaInfo(BaseModel):
    object_type: str = Field(default="schema")
    name: str = Field(default="")
    tables: list[TableInfo] = Field(default_factory=list)


def get_schema_info(metadata: sa.MetaData) -> SchemaInfo:
    tables = list()
    for table_name, table in metadata.tables.items():
        table_info = get_table_info(table)
        # rprint(table_info.model_dump()) # for debug only
        tables.append(table_info)

    return SchemaInfo(
        name=metadata.schema or "",
        tables=tables,
    )
