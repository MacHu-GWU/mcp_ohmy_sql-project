# -*- coding: utf-8 -*-

"""
Constant variables used in this project.
"""

import typing as T
import os

from enum_mate.api import BetterStrEnum
from pydantic import BaseModel, Field

TAB = " " * 2


class LLMColumnConstraintEnum(BetterStrEnum):
    """
    Simplified database column constraints optimized for LLM token efficiency.
    Used in schema encoding to reduce token usage while preserving essential constraint information.
    """

    # relational database
    PK = "PK"  # Primary Key
    UQ = "UQ"  # Unique Key
    IDX = "IDX"  # Index
    FK = "FK"  # Foreign Key
    NN = "NN"  # Not Null
    # aws redshift
    DK = "DK"  # Distribution Key
    SK = "SK"  # Sort Key


class LLMTypeEnum(BetterStrEnum):
    """
    Simplified database column data types optimized for LLM token efficiency.
    Used in schema encoding to represent SQL data types with minimal tokens while preserving semantic meaning.
    """

    STR = "str"  # String/text data of any length
    INT = "int"  # Whole numbers without decimal points
    FLOAT = "float"  # Approximate decimal numbers (IEEE floating point)
    DEC = "dec"  # Exact decimal numbers for currency/financial data
    DT = "dt"  # Date and time combined (local timezone)
    TS = "ts"  # Timestamp with timezone information (UTC)
    DATE = "date"  # Date only without time component
    TIME = "time"  # Time only without date component
    BLOB = "blob"  # Large binary files (images, documents)
    BIN = "bin"  # Small fixed-length binary data (hashes, UUIDs)
    BOOL = "bool"  # True/false boolean values
    NULL = "null"  # Null Type, represents no value


class ObjectTypeEnum(BetterStrEnum):
    """
    Database object types for categorizing different database entities.
    Used in schema introspection and metadata processing to identify object types.
    """

    FOREIGN_KEY = "foreign key"
    COLUMN = "column"
    TABLE = "table"
    VIEW = "view"
    MATERIALIZED_VIEW = "materialized view"
    SCHEMA = "schema"
    DATABASE = "database"

    @property
    def table_type(self) -> "TableTypeEnum":
        return db_object_type_to_table_type_mapping[self]


# [startdbtypeenum]
class DbTypeEnum(BetterStrEnum):
    """
    Supported database system types for connection configuration.
    Used in configuration validation and connection factory selection.
    """

    SQLITE = "sqlite"  # SQLite local databases
    POSTGRESQL = "postgresql"  # PostgreSQL databases
    MYSQL = "mysql"  # MySQL/MariaDB databases
    MSSQL = "mssql"  # Microsoft SQL Server
    ORACLE = "oracle"  # Oracle databases
    AWS_REDSHIFT = "aws_redshift"  # Amazon Redshift data warehouses
    SNOWFLAKE = "snowflake"  # Snowflake cloud databases
    MONGODB = "mongodb"  # MongoDB with SQL interface
    ELASTICSEARCH = "elasticsearch"  # Elasticsearch with SQL
    OPENSEARCH = "opensearch"  # OpenSearch with SQL


# [enddbtypeenum]


class TableTypeEnum(BetterStrEnum):
    """
    Database table types for distinguishing between tables, views, and materialized views.
    Used in schema introspection and metadata categorization for proper object identification.
    """

    TABLE = "Table"
    VIEW = "View"
    MATERIALIZED_VIEW = "MaterializedView"


db_object_type_to_table_type_mapping = {
    ObjectTypeEnum.TABLE: TableTypeEnum.TABLE,
    ObjectTypeEnum.VIEW: TableTypeEnum.VIEW,
    ObjectTypeEnum.MATERIALIZED_VIEW: TableTypeEnum.MATERIALIZED_VIEW,
}


class EnvVar(BaseModel):
    """
    Environment variable wrapper with default value support.
    Used for accessing environment variables throughout the application with fallback defaults.
    """

    name: str = Field()
    default: str = Field(default="")

    @property
    def value(self) -> str:
        return os.environ.get(self.name, self.default)


class EnvVarEnum:
    """
    Collection of predefined environment variables used throughout the application.
    Used for centralized environment variable management and configuration loading.
    """

    MCP_OHMY_SQL_CONFIG = EnvVar(name="MCP_OHMY_SQL_CONFIG")
