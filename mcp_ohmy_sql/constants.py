# -*- coding: utf-8 -*-

import typing as T
import os

from enum_mate.api import BetterStrEnum
from pydantic import BaseModel, Field

TAB = " " * 2


class LLMColumnConstraintEnum(BetterStrEnum):
    """
    Enum representing simplified LLM-friendly constraints for database columns.
    These constraints are designed to be concise while retaining essential information.
    """

    PK = "PK"  # Primary Key
    UQ = "UQ"  # Unique Key
    IDX = "IDX"  # Index
    FK = "FK"  # Foreign Key
    NN = "NN"  # Not Null


class LLMTypeEnum(BetterStrEnum):
    """
    Enum representing simplified LLM-friendly types for database columns.
    These types are designed to be concise while retaining essential information.
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
    FOREIGN_KEY = "foreign key"
    COLUMN = "column"
    TABLE = "table"
    VIEW = "view"
    MATERIALIZED_VIEW = "materialized view"
    SCHEMA = "schema"
    DATABASE = "database"


class DbTypeEnum(BetterStrEnum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MSSQL = "mssql"
    ORACLE = "oracle"
    AWS_REDSHIFT = "aws_redshift"
    ELASTICSEARCH = "elasticsearch"
    OPENSEARCH = "opensearch"
    SNOWFLAKE = "snowflake"
    MONGODB = "mongodb"


class TableTypeEnum(BetterStrEnum):
    TABLE = "Table"
    VIEW = "View"
    MATERIALIZED_VIEW = "MaterializedView"


class EnvVar(BaseModel):
    name: str = Field()
    default: str = Field(default="")

    @property
    def value(self) -> str:
        return os.environ.get(self.name, self.default)


class EnvVarEnum:
    MCP_OHMY_SQL_CONFIG = EnvVar(name="MCP_OHMY_SQL_CONFIG")
