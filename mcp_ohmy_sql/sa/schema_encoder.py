# -*- coding: utf-8 -*-

"""
A utility module that converts SQLAlchemy metadata objects into LLM-friendly
schema representations. This module transforms verbose database schema information
into compact, semantically clear formats optimized for Large Language Model
consumption in text-to-SQL applications, significantly reducing token usage
while preserving essential structural and constraint information.
"""

import textwrap

from ..constants import (
    TAB,
    PK,
    UQ,
    IDX,
    FK,
    NN,
    TableTypeEnum,
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

    Format: ${COLUMN_NAME}:${DATA_TYPE}${PRIMARY_KEY}${UNIQUE}${NOT_NULL}${INDEX}${FOREIGN_KEY}

    .. note::

        There might be multiple Foreign Keys encoded as ``*FK->Table1.Column1*FK->Table2.Column2``.

    Constraints are encoded as:

    - ``*PK``: Primary Key (implies unique and indexed)
    - ``*UQ``: Unique constraint (implies indexed)
    - ``*NN``: Not Null constraint
    - ``*IDX``: Has database index
    - ``*FK->Table.Column``: Foreign key reference

    Redundant constraints are automatically omitted (PK/UQ don't show IDX).

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


TABLE_TYPE_NAME_MAPPING: dict[str, str] = {
    TableTypeEnum.TABLE.value: "Table",
    TableTypeEnum.VIEW.value: "View",
    TableTypeEnum.MATERIALIZED_VIEW.value: "MaterializedView",
}


def encode_table_info(
    table_info: TableInfo,
) -> str:
    """
    Encode a database table into LLM-friendly compact format.

    Format::

        Table TableName(
            encoded_column_info_1,
            encoded_column_info_2,
            ...
        )

    This format provides:

    - Immediate visual structure similar to SQL CREATE TABLE
    - Compact representation reducing token usage by ~70%
    - Preserves all essential schema information
    - Self-documenting constraint annotations
    - Clear foreign key relationships

    :param table_info: Table metadata containing columns and foreign keys

    :returns: Compact table representation string

    Example::

        Table Product(
            ProductId:INT*PK,
            ProductName:STR*NN,
            CategoryId:INT*NN*FK->Category.CategoryId,
            Price:DEC*NN,
            Stock:INT*NN,
            CreatedAt:TS*NN,
            UpdatedAt:TS
        )

        # or
        View SalesReport(
            ...
        )

        # or
        MaterializedView MonthlySales(
            ...
        )
    """
    columns = list()
    for col in table_info.columns:
        col_str = encode_column_info(table_info, col)
        columns.append(f"{TAB}{col_str},")
    columns_def = "\n".join(columns)
    text = f"{TABLE_TYPE_NAME_MAPPING[table_info.object_type]} {table_info.name}(\n{columns_def}\n)"
    return text


def encode_schema_info(
    schema_info: SchemaInfo,
) -> str:
    """
    Encode a database schema into LLM-friendly compact format.

    Format::

        Schema SchemaName(
            encoded_table_info_1,
            encoded_table_info_2,
            ...,
        )

    Key benefits for LLM consumption:

    - **Token Efficiency**: Reduces schema representation by ~70% compared to
      verbose SQL DDL or JSON formats
    - **Semantic Clarity**: Constraint abbreviations (PK, FK, NN) are intuitive
      and consistently applied
    - **Relationship Visibility**: Foreign keys show target table/column inline,
      enabling quick relationship understanding
    - **Type Simplification**: Database-specific types mapped to universal
      categories (STR, INT, DEC, etc.)
    - **Hierarchical Structure**: Clear nesting shows schema->table->column
      relationships

    :param schema_info: Schema metadata containing all tables and relationships

    :returns: Compact schema representation string

    Example::

        Schema ecommerce(
            Table Customer(
                CustomerId:INT*PK,
                Email:STR*UQ*NN,
                FirstName:STR*NN,
                LastName:STR*NN,
                CreatedAt:TS*NN
            ),
            Table Order(
                OrderId:INT*PK,
                CustomerId:INT*NN*FK->Customer.CustomerId,
                OrderDate:DT*NN,
                TotalAmount:DEC*NN,
                Status:STR*NN
            ),
            Table OrderItem(
                OrderItemId:INT*PK,
                OrderId:INT*NN*FK->Order.OrderId,
                ProductId:INT*NN*FK->Product.ProductId,
                Quantity:INT*NN,
                UnitPrice:DEC*NN
            )
        )
    """
    tables = list()
    for table in schema_info.tables:
        table_str = encode_table_info(table)
        tables.append(textwrap.indent(table_str, prefix=TAB))
    tables_def = "\n".join(tables)
    if schema_info.name:  # pragma: no cover
        schema_name = schema_info.name
    else:
        schema_name = "default"
    text = f"Schema {schema_name}(\n{tables_def}\n)"
    return text
