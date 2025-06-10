# -*- coding: utf-8 -*-

"""
SQLAlchemy type mapping module for mcp_ohmy_sql.

This module provides utilities for mapping SQLAlchemy type objects to simplified
type representations suitable for LLM consumption. It handles both generic SQLAlchemy
types (e.g., String, Integer) and SQL standard types (e.g., VARCHAR, BIGINT).

The main component is the ColumnType class which provides a standardized way to
represent database column types with both full type names and simplified LLM-friendly
names that save tokens while retaining essential type information.
"""

from pydantic import BaseModel, Field
from sqlalchemy.types import TypeEngine

from ..constants import (
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

SQLALCHEMY_TYPE_MAPPING = {
    # String type
    "string": STR,  # String
    "text": STR,  # Text
    "unicode": STR,  # Unicode
    "unicode_text": STR,  # UnicodeText
    "VARCHAR": STR,  # VARCHAR
    "NVARCHAR": STR,  # NVARCHAR
    "CHAR": STR,  # CHAR
    "NCHAR": STR,  # NCHAR
    "TEXT": STR,  # TEXT
    "CLOB": STR,  # CLOB
    # Integer type
    "integer": INT,  # Integer
    "small_integer": INT,  # SmallInteger
    "big_integer": INT,  # BigInteger
    "INTEGER": INT,  # INTEGER
    "SMALLINT": INT,  # SMALLINT
    "BIGINT": INT,  # BIGINT
    # float type
    "float": FLOAT,  # Float
    "double": FLOAT,  # Double
    "REAL": FLOAT,  # REAL
    "FLOAT": FLOAT,  # FLOAT
    "DOUBLE": FLOAT,  # DOUBLE
    "DOUBLE_PRECISION": FLOAT,  # DOUBLE_PRECISION
    # decimal type
    "numeric": DEC,  # Numeric
    "NUMERIC": DEC,  # NUMERIC
    "DECIMAL": DEC,  # DECIMAL
    # 时间日期类型
    "datetime": DT,  # DateTime
    "DATETIME": DT,  # DATETIME
    "TIMESTAMP": TS,  # TIMESTAMP
    "date": DATE,  # Date
    "DATE": DATE,  # DATE
    "time": TIME,  # Time
    "TIME": TIME,  # TIME
    # 二进制类型
    "large_binary": BLOB,  # LargeBinary
    "BLOB": BLOB,  # BLOB
    "BINARY": BIN,  # BINARY
    "VARBINARY": BIN,  # VARBINARY
    # 布尔类型
    "boolean": BOOL,  # Boolean
    "BOOLEAN": BOOL,  # BOOLEAN
    # 特殊类型
    "enum": STR,  # Enum (存储为字符串)
    "JSON": STR,  # JSON
    "uuid": STR,  # Uuid (默认存储格式)
    "UUID": STR,  # UUID
    "null": NULL,  # NullType
    # Additional types not in original mapping
    "ARRAY": STR,  # ARRAY
    "type_decorator": STR,  # TypeDecorator (PickleType, Interval, Variant)
    "user_defined": STR,  # UserDefinedType
}
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


class ColumnType(BaseModel):
    """
    Represents a column type in the database.

    This class provides a standardized way to represent database column types with:
    - name: The full SQLAlchemy type representation (e.g., "VARCHAR(255)", "INTEGER")
    - llm_name: A simplified type constant for LLM consumption (e.g., "STR", "INT")

    The llm_name field uses predefined constants that are more concise while retaining
    essential type information, helping to reduce token usage in LLM interactions.

    :param name: The full string representation of the SQLAlchemy type
    :param llm_name: The simplified type name using predefined constants (STR, INT, etc.)
    """

    name: str = Field()
    llm_name: str = Field()

    @classmethod
    def from_type(cls, type_: "TypeEngine"):
        """
        Create a ColumnType instance from a SQLAlchemy TypeEngine object.

        This method extracts type information from a SQLAlchemy type object and maps it
        to our simplified type system. It uses the type's visit_name attribute for mapping
        when available, falling back to the string representation for unknown types.

        :param type_: A SQLAlchemy TypeEngine instance representing a column type

        :returns: A new ColumnType instance with mapped type information

        Example:
            >>> from sqlalchemy import String, Integer, DECIMAL
            >>> ColumnType.from_type(String(50))
            ColumnType(name='VARCHAR(50)', llm_name='STR')
            >>> ColumnType.from_type(Integer())
            ColumnType(name='INTEGER', llm_name='INT')
            >>> ColumnType.from_type(DECIMAL(10, 2))
            ColumnType(name='DECIMAL(10, 2)', llm_name='DEC')
        """
        # Get the string representation of the type (includes parameters like VARCHAR(50))
        name = str(type_)

        # Try to get the visit name for type mapping
        visit_name = getattr(type_, "__visit_name__", None)

        # Map to simplified LLM type, fallback to full name if not in mapping
        llm_name = SQLALCHEMY_TYPE_MAPPING.get(visit_name, name) if visit_name else name

        return cls(name=name, llm_name=llm_name)
