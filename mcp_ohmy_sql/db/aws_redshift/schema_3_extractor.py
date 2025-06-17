# -*- coding: utf-8 -*-

import typing as T
import sqlalchemy as sa
from sqlalchemy.types import TypeEngine

from ...constants import ObjectTypeEnum, DbTypeEnum, LLMTypeEnum
from ...utils import match

from .sql import SqlEnum
from .schema_1_model import (
    ColumnInfo,
    TableInfo,
    SchemaInfo,
    DatabaseInfo,
)

try:
    from rich import print as rprint
except ImportError:  # pragma: no cover
    pass


def sqlalchemy_type_to_llm_type(type_: TypeEngine) -> LLMTypeEnum:
    """
    Convert SQLAlchemy type objects to simplified type representations suitable
    for LLM consumption. It handles both generic SQLAlchemy types
    (e.g., String, Integer) and SQL standard types (e.g., VARCHAR, BIGINT).

    :param type_: A SQLAlchemy TypeEngine instance representing a column type

    :returns: A new ColumnType instance with mapped type information

    Example:
        >>> from sqlalchemy import String, Integer, DECIMAL
        >>> sqlalchemy_type_to_llm_type(String(50))
        'STR'
        >>> sqlalchemy_type_to_llm_type(Integer())
        'INT'
        >>> sqlalchemy_type_to_llm_type(DECIMAL(10, 2))
        'DEC'
    """
    # Get the string representation of the type (includes parameters like VARCHAR(50))
    type_name = str(type_)
    # Try to get the visit name for type mapping
    visit_name = getattr(type_, "__visit_name__", None)
    # Map to simplified LLM type, fallback to full name if not in mapping
    llm_type_name = (
        SQLALCHEMY_TYPE_MAPPING.get(visit_name, type_name) if visit_name else type_name
    )
    return llm_type_name


def new_column_info(
    table: sa.Table,
    column: sa.Column,
) -> ColumnInfo:
    foreign_keys = list()
    for foreign_key in column.foreign_keys:
        foreign_key_info = new_foreign_key_info(foreign_key)
        # rprint(foreign_key_info.model_dump())  # for debug only
        foreign_keys.append(foreign_key_info)
    column_info = ColumnInfo(
        name=column.name,
        fullname=f"{table.name}.{column.name}",
        type=str(column.type),
        llm_type=sqlalchemy_type_to_llm_type(column.type),
        primary_key=column.primary_key,
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
    # rprint(column_info.model_dump())  # for debug only
    return column_info


def new_table_info(
    table: sa.Table,
    object_type: ObjectTypeEnum,
) -> TableInfo:
    foreign_keys = list()
    for foreign_key in table.foreign_keys:
        foreign_key_info = new_foreign_key_info(foreign_key)
        # rprint(foreign_key_info.model_dump())  # for debug only
        foreign_keys.append(foreign_key_info)

    columns = list()
    for _, column in table.columns.items():
        column_info = new_column_info(table=table, column=column)
        # rprint(column_info.model_dump())  # for debug only
        columns.append(column_info)

    table_info = TableInfo(
        object_type=object_type,
        name=table.name,
        comment=table.comment,
        fullname=table.fullname,
        primary_key=[col.name for col in table.primary_key.columns],
        foreign_keys=foreign_keys,
        columns=columns,
    )
    # rprint(table_info.model_dump())  # for debug only
    return table_info


def new_schema_info(
    engine: sa.engine.Engine,
    metadata: sa.MetaData,
    schema_name: T.Optional[str] = None,
    include: T.Optional[list[str]] = None,
    exclude: T.Optional[list[str]] = None,
) -> SchemaInfo:
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
    for table in metadata.sorted_tables:
        table_name = table.name
        # don't include tables from other schemas
        if table.schema != schema_name:  # pragma: no cover
            continue
        # don't include tables that don't match the criteria
        if match(table_name, include, exclude) is False:
            continue

        if table_name in view_names:  # pragma: no cover
            object_type = ObjectTypeEnum.VIEW
        elif table_name in materialized_view_names:  # pragma: no cover
            object_type = ObjectTypeEnum.MATERIALIZED_VIEW
        else:
            object_type = ObjectTypeEnum.TABLE
        table_info = new_table_info(table=table, object_type=object_type)
        # rprint(table_info.model_dump()) # for debug only
        tables.append(table_info)

    schema_info = SchemaInfo(
        name=metadata.schema or "",
        tables=tables,
    )
    # rprint(schema_info.model_dump()) # for debug only
    return schema_info


def new_database_info(
    name: str,
    db_type: DbTypeEnum,
    schemas: list[SchemaInfo],
    comment: T.Optional[str] = None,
) -> DatabaseInfo:
    database_info = DatabaseInfo(
        name=name,
        comment=comment,
        db_type=db_type,
        schemas=schemas,
    )
    # rprint(database_info.model_dump()) # for debug only
    return database_info
