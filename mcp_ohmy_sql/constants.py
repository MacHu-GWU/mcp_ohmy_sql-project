# -*- coding: utf-8 -*-

import os
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


class EnvVar(BaseModel):
    name: str = Field()
    default: str = Field(default="")

    @property
    def value(self) -> str:
        return os.environ.get(self.name, self.default)


class EnvVarNameEnum:
    MCP_OHMY_SQL_CONFIG = EnvVar(name="MCP_OHMY_SQL_CONFIG")
