# -*- coding: utf-8 -*-

import typing as T
import os

from enum_mate.api import BetterStrEnum
from pydantic import BaseModel, Field

TAB = " " * 2

PK = "PK"  # Primary Key
UQ = "UQ"  # Unique Key
IDX = "IDX"  # Index
FK = "FK"  # Foreign Key
NN = "NN"  # Not Null

STR = "STR"  # String/text data of any length
INT = "INT"  # Whole numbers without decimal points
FLOAT = "FLOAT"  # Approximate decimal numbers (IEEE floating point)
DEC = "DEC"  # Exact decimal numbers for currency/financial data
DT = "DT"  # Date and time combined (local timezone)
TS = "TS"  # Timestamp with timezone information (UTC)
DATE = "DATE"  # Date only without time component
TIME = "TIME"  # Time only without date component
BLOB = "BLOB"  # Large binary files (images, documents)
BIN = "BIN"  # Small fixed-length binary data (hashes, UUIDs)
BOOL = "BOOL"  # True/false boolean values
NULL = "NULL"  # Null Type, represents no value


TABLE_TYPE_TABLE: T.Final = "table"
TABLE_TYPE_VIEW: T.Final = "view"
TABLE_TYPE_MATERIALIZED_VIEW: T.Final = "materialized_view"


class TableTypeEnum(BetterStrEnum):
    TABLE = "table"
    VIEW = "view"
    MATERIALIZED_VIEW = "materialized_view"


class EnvVar(BaseModel):
    name: str = Field()
    default: str = Field(default="")

    @property
    def value(self) -> str:
        return os.environ.get(self.name, self.default)


class EnvVarEnum:
    MCP_OHMY_SQL_CONFIG = EnvVar(name="MCP_OHMY_SQL_CONFIG")
