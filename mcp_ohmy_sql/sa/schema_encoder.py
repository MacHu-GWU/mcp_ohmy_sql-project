# -*- coding: utf-8 -*-

"""
A utility module that converts SQLAlchemy metadata objects into LLM-friendly
schema representations. This module transforms verbose database schema information
into compact, semantically clear formats optimized for Large Language Model
consumption in text-to-SQL applications, significantly reducing token usage
while preserving essential structural and constraint information.
"""

import typing as T
import textwrap

from ..constants import (
    TAB,
    PK,
    UQ,
    IDX,
    FK,
    NN,
    STR,
    INT,
    FLOAT,
    DEC,
    DT,
    TS,
    DATE,
    TIME,
    BLOB,
    BIN,
    BOOL,
    NULL,
)
from .metadata import (
    ForeignKeyInfo,
    ColumnInfo,
    TableInfo,
    SchemaInfo,
)
from .metadata import (
    ColumnInfo,
    TableInfo,
    SchemaInfo,
)


def encode_column_info(
    table_info: TableInfo,
    column_info: ColumnInfo,
) -> str:
    """
    Encode a database column into LLM-friendly compact format.

    Transforms verbose column metadata into a concise string representation
    optimized for Large Language Model consumption in text-to-SQL tasks.

    Format: ${ColumnName}:${TYPE}${PRIMARY_KEY}${UNIQUE}${NOT_NULL}${INDEX}${FOREIGN_KEY}

    .. note::

        There might be multiple Foreign Keys encoded as ``*FK->Table1.Column1*FK->Table2.Column2``.

    Constraints are encoded as:

    - *PK: Primary Key (implies unique and indexed)
    - *UQ: Unique constraint (implies indexed)
    - *NN: Not Null constraint
    - *IDX: Has database index
    - *FK->Table.Column: Foreign key reference

    Redundant constraints are automatically omitted (PK/UQ don't show *IDX).

    :param table_info: Table metadata containing primary key information
    :param column_info: Column metadata with type, constraints, and relationships

    :returns: Compact column representation string

    Examples:

    - Primary key column: ``UserId:INT*PK``
    - Foreign key with index: ``CategoryId:INT*NN*IDX*FK->Category.CategoryId``
    - Unique email field: ``Email:STR*UQ*NN``
    - Simple nullable column: ``Description:STR``
    """
    col_name = column_info.name
    col_type = column_info.type.llm_name
    pk = f"*{PK}" if column_info.name in table_info.primary_key else ""
    uq = f"*{UQ}" if column_info.unique else ""
    nn = f"*{NN}" if not column_info.nullable else ""
    idx = f"*{IDX}" if column_info.index else ""
    # If the column is a primary key or unique, by default it is indexed.
    if pk or uq:
        idx = ""
    fk_list = list()
    for fk in column_info.foreign_keys:
        fk_list.append(f"*{FK}->{fk.name}")
    fk = "".join(fk_list)

    text = f"{col_name}:{col_type}{pk}{uq}{nn}{idx}{fk}"
    return text


def encode_table_info(
    table_info: TableInfo,
) -> str:
    """
    Encode a database table into LLM-friendly compact format.

    Transforms verbose table metadata into a concise string representation
    optimized for Large Language Model consumption in text-to-SQL tasks.

    :param table_info: Table metadata containing columns and foreign keys

    :returns: Compact table representation string
    """
    columns = list()
    for col in table_info.columns:
        col_str = encode_column_info(table_info, col)
        columns.append(f"{TAB}{col_str},")
    columns_def = "\n".join(columns)
    text = f"Table {table_info.name}(\n{columns_def}\n)"
    return text


def encode_schema_info(
    schema_info: SchemaInfo,
) -> str:
    """
    Encode a database schema into LLM-friendly compact format.

    :returns: Compact schema representation string
    """
    tables = list()
    for table in schema_info.tables:
        table_str = encode_table_info(table)
        tables.append(textwrap.indent(table_str, prefix=TAB))
    tables_def = "\n".join(tables)
    if schema_info.name:
        schema_name = schema_info.name
    else:
        schema_name = "default"
    text = f"Schema {schema_name}{{\n{tables_def}\n}}"
    return text
