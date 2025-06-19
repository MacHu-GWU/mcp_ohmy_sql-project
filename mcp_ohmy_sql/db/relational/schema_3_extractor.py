# -*- coding: utf-8 -*-

import typing as T

from ...lazy_import import sa, TypeEngine, Library

from ...constants import ObjectTypeEnum, DbTypeEnum, LLMTypeEnum
from ...utils import match

from .schema_1_model import (
    ForeignKeyInfo,
    ColumnInfo,
    TableInfo,
    SchemaInfo,
    DatabaseInfo,
)

try:
    from rich import print as rprint
except ImportError:  # pragma: no cover
    pass


def get_sqlalchemy_type_mapping() -> dict[str, LLMTypeEnum]:
    """
    Get the SQLAlchemy type mapping dictionary.

    This function returns a dictionary that maps SQLAlchemy type visit names
    to simplified LLM type constants. It is used to convert SQLAlchemy types
    to a format suitable for LLM consumption.
    """
    if isinstance(sa, Library):  # pragma: no cover
        return {}
    else:
        return {
            # String type
            sa.String.__visit_name__: LLMTypeEnum.STR,
            sa.Text.__visit_name__: LLMTypeEnum.STR,
            sa.Unicode.__visit_name__: LLMTypeEnum.STR,
            sa.UnicodeText.__visit_name__: LLMTypeEnum.STR,
            sa.VARCHAR.__visit_name__: LLMTypeEnum.STR,
            sa.NVARCHAR.__visit_name__: LLMTypeEnum.STR,
            sa.CHAR.__visit_name__: LLMTypeEnum.STR,
            sa.NCHAR.__visit_name__: LLMTypeEnum.STR,
            sa.TEXT.__visit_name__: LLMTypeEnum.STR,
            sa.CLOB.__visit_name__: LLMTypeEnum.STR,
            # Integer type
            sa.Integer.__visit_name__: LLMTypeEnum.INT,
            sa.SmallInteger.__visit_name__: LLMTypeEnum.INT,
            sa.BigInteger.__visit_name__: LLMTypeEnum.INT,
            sa.INTEGER.__visit_name__: LLMTypeEnum.INT,
            sa.SMALLINT.__visit_name__: LLMTypeEnum.INT,
            sa.BIGINT.__visit_name__: LLMTypeEnum.INT,
            # float type
            sa.Float.__visit_name__: LLMTypeEnum.FLOAT,
            sa.Double.__visit_name__: LLMTypeEnum.FLOAT,
            sa.REAL.__visit_name__: LLMTypeEnum.FLOAT,
            sa.FLOAT.__visit_name__: LLMTypeEnum.FLOAT,
            sa.DOUBLE.__visit_name__: LLMTypeEnum.FLOAT,
            sa.DOUBLE_PRECISION.__visit_name__: LLMTypeEnum.FLOAT,
            # decimal type
            sa.Numeric.__visit_name__: LLMTypeEnum.DEC,
            sa.NUMERIC.__visit_name__: LLMTypeEnum.DEC,
            sa.DECIMAL.__visit_name__: LLMTypeEnum.DEC,
            # datetime
            sa.DateTime.__visit_name__: LLMTypeEnum.DT,
            sa.DATETIME.__visit_name__: LLMTypeEnum.DT,
            sa.TIMESTAMP.__visit_name__: LLMTypeEnum.TS,
            sa.Date.__visit_name__: LLMTypeEnum.DATE,
            sa.DATE.__visit_name__: LLMTypeEnum.DATE,
            sa.Time.__visit_name__: LLMTypeEnum.TIME,
            sa.TIME.__visit_name__: LLMTypeEnum.TIME,
            # binary type
            sa.LargeBinary.__visit_name__: LLMTypeEnum.BLOB,
            sa.BLOB.__visit_name__: LLMTypeEnum.BLOB,
            sa.BINARY.__visit_name__: LLMTypeEnum.BIN,
            sa.VARBINARY.__visit_name__: LLMTypeEnum.BIN,
            # bool type
            sa.Boolean.__visit_name__: LLMTypeEnum.BOOL,
            sa.BOOLEAN.__visit_name__: LLMTypeEnum.BOOL,
            # special types
            sa.Enum.__visit_name__: LLMTypeEnum.STR,  #  (stored as string)
            sa.JSON.__visit_name__: LLMTypeEnum.STR,
            sa.Uuid.__visit_name__: LLMTypeEnum.STR,  #  (default storage format)
            sa.UUID.__visit_name__: LLMTypeEnum.STR,
            sa.Null.__visit_name__: LLMTypeEnum.NULL,
            # Additional types not in original mapping
            sa.ARRAY.__visit_name__: LLMTypeEnum.STR,  #
            sa.TypeDecorator.__visit_name__: LLMTypeEnum.STR,  #  (PickleType, Interval, Variant)
        }


SQLALCHEMY_TYPE_MAPPING = get_sqlalchemy_type_mapping()
"""
Mapping from SQLAlchemy type visit names to simplified LLM type constants.

This dictionary maps SQLAlchemy's internal type visit names (used for type introspection)
to our simplified type constants that are more suitable for LLM consumption. The mapping
covers all standard SQLAlchemy types including:

- Generic types (e.g., String, Integer, Float)
- SQL standard types (e.g., VARCHAR, BIGINT, TIMESTAMP)
- Special types (e.g., JSON, UUID, Enum)

The visit name is accessed via type.__visit_name__ for each SQLAlchemy type instance.
"""


def sqlalchemy_type_to_llm_type(type_: TypeEngine) -> LLMTypeEnum:
    """
    Convert SQLAlchemy type objects to simplified type representations suitable
    for LLM consumption. It handles both generic SQLAlchemy types
    (e.g., String, Integer) and SQL standard types (e.g., VARCHAR, BIGINT).

    :param type_: A SQLAlchemy TypeEngine instance representing a column type

    :returns: A new llm type name

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


def new_foreign_key_info(
    foreign_key: "sa.ForeignKey",
) -> ForeignKeyInfo:
    foreign_key_info = ForeignKeyInfo(
        name=str(foreign_key.column),
        comment=foreign_key.comment,
        onupdate=foreign_key.onupdate,
        ondelete=foreign_key.ondelete,
        deferrable=foreign_key.deferrable,
        initially=foreign_key.initially,
    )
    # rprint(foreign_key_info.model_dump())  # for debug only
    return foreign_key_info


def new_column_info(
    table: "sa.Table",
    column: "sa.Column",
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
    table: "sa.Table",
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
    engine: "sa.engine.Engine",
    metadata: "sa.MetaData",
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
