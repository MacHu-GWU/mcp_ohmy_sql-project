# -*- coding: utf-8 -*-

"""
This module provides utilities for mapping AWS Redshift schema models to simplified
type representations suitable for LLM consumption.
"""

from ...constants import LLMColumnConstraintEnum

from .tpl import TemplateEnum
from .schema_1_model import (
    ColumnInfo,
    TableInfo,
    SchemaInfo,
    DatabaseInfo,
)


def encode_column_info(
    column_info: ColumnInfo,
) -> str:
    """
    Encode an AWS Redshift column into LLM-friendly compact format.

    Transforms verbose column metadata into a concise string representation
    optimized for Large Language Model consumption in text-to-SQL tasks.

    Format: ${COLUMN_NAME}:${DATA_TYPE}${DISTRIBUTION_KEY}${SORT_KEY}${NOT_NULL}${ENCODING}

    Redshift-specific constraints are encoded as:

    - ``*DK``: Distribution Key (for data distribution across nodes)
    - ``*SK-N``: Sort Key with position N (for query optimization)
    - ``*NN``: Not Null constraint
    - ``*encoding``: Compression encoding (lzo, delta, etc.)

    :param column_info: Column metadata with Redshift-specific properties

    :returns: Compact column representation string

    Examples:

    - Distribution key: ``user_id:str*DK*NN*lzo``
    - Sort key: ``create_time:dt*SK-1*NN*delta``
    - Regular column: ``description:str*lzo``
    """
    col_name = column_info.name
    col_type = column_info.llm_type.value if column_info.llm_type else column_info.type
    dk = f"*{LLMColumnConstraintEnum.DK.value}" if column_info.dist_key else ""
    sk = (
        f"*{LLMColumnConstraintEnum.SK.value}-{column_info.sort_key_position}"
        if column_info.sort_key_position
        else ""
    )
    nn = f"*{LLMColumnConstraintEnum.NN.value}" if column_info.notnull else ""
    encoding = f"*{column_info.encoding}"
    text = f"{col_name}:{col_type}{dk}{sk}{nn}{encoding}"
    return text


def encode_table_info(
    table_info: TableInfo,
) -> str:
    """
    Encode an AWS Redshift table into LLM-friendly compact format.

    Format::

        Table TableName DistributionStyle Distribution Style (
            encoded_column_info_1,
            encoded_column_info_2,
            ...
        )

    Redshift-specific features:

    - **Distribution Style**: Shows how data is distributed (KEY, EVEN, ALL)
    - **Distribution Keys**: Indicates which columns control data distribution
    - **Sort Keys**: Shows column ordering for query optimization
    - **Compression**: Displays encoding for each column

    :param table_info: Table metadata with Redshift-specific properties

    :returns: Compact table representation string

    Example::

        Table users KEY Distribution Style (
            user_id:str*DK*NN*lzo,
            create_time:dt*SK-1*NN*delta,
            description:str*lzo,
        )
    """
    table_type_name = table_info.object_type.table_type.value
    table_name = table_info.name
    dist_style = table_info.dist_style
    columns = list()
    for column_info in table_info.columns:
        column = encode_column_info(column_info)
        columns.append(column)
    text = TemplateEnum.table_info.render(
        table_type_name=table_type_name,
        table_name=table_name,
        dist_style=dist_style,
        columns=columns,
    )
    return text


def encode_schema_info(
    schema_info: SchemaInfo,
) -> str:
    """
    Encode an AWS Redshift schema into LLM-friendly compact format.

    Format::

        Schema SchemaName (
            encoded_table_info_1,
            encoded_table_info_2,
            ...,
        )

    Key benefits for LLM consumption:

    - **Redshift Optimization**: Highlights distribution and sort keys for
      query performance understanding
    - **Compression Visibility**: Shows encoding schemes for storage optimization
    - **Token Efficiency**: Compact format reduces token usage while preserving
      Redshift-specific metadata
    - **Performance Hints**: Distribution and sort key information helps LLMs
      generate optimized queries

    :param schema_info: Schema metadata containing Redshift tables

    :returns: Compact schema representation string

    Example::

        Schema public (
            Table users KEY Distribution Style (
                user_id:str*DK*NN*lzo,
                create_time:dt*SK-1*NN*delta,
                description:str*lzo,
            ),
            Table orders EVEN Distribution Style (
                order_id:int*PK*NN*delta,
                user_id:str*NN*FK->users.user_id*lzo,
                order_date:dt*SK-1*NN*delta,
            ),
        )
    """
    tables = list()
    for table_info in schema_info.tables:
        table = encode_table_info(table_info)
        tables.append(table)
    text = TemplateEnum.schema_info.render(
        schema_name=schema_info.name,
        schema_description=schema_info.comment if schema_info.comment else "",
        tables=tables,
    )
    return text


def encode_database_info(
    database_info: DatabaseInfo,
) -> str:
    """
    Encode an AWS Redshift database into LLM-friendly compact format.

    Format::

        aws_redshift Database DatabaseName (
            Schema SchemaName (
                encoded_table_info_1,
                encoded_table_info_2,
                ...,
            ),
            ...
        )

    Redshift-specific considerations:

    - **Cluster Architecture**: Represents the distributed nature of Redshift
    - **Performance Metadata**: Includes distribution and sort key information
      critical for query optimization
    - **Compression Details**: Encoding information for storage efficiency
    - **Multi-Schema Support**: Handles multiple schemas within a cluster

    :param database_info: Database metadata with Redshift-specific schemas

    :returns: Compact database representation string

    Example::

        aws_redshift Database mcp_ohmy_sql_dev (
            Schema public (
                Table users KEY Distribution Style (
                    user_id:str*DK*NN*lzo,
                    create_time:dt*SK-1*NN*delta,
                ),
            ),
            Schema analytics (
                Table daily_metrics EVEN Distribution Style (
                    metric_date:dt*SK-1*NN*delta,
                    metric_value:dec*NN*delta,
                ),
            ),
        )
    """
    schemas = list()
    for schema_info in database_info.schemas:
        schema = encode_schema_info(schema_info)
        schemas.append(schema)
    text = TemplateEnum.database_info.render(
        database_type=database_info.db_type.value,
        database_name=database_info.name,
        database_description=database_info.comment if database_info.comment else "",
        schemas=schemas,
    )
    return text
