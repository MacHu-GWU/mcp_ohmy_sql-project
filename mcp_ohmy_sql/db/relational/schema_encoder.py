# -*- coding: utf-8 -*-

"""
This module provides utilities for mapping SQLAlchemy type objects to simplified
type representations suitable for LLM consumption. It handles both generic SQLAlchemy
types (e.g., String, Integer) and SQL standard types (e.g., VARCHAR, BIGINT).
"""

from pydantic import BaseModel, Field
import sqlalchemy as sa
from sqlalchemy.types import TypeEngine

from ...constants import LLMTypeEnum

SQLALCHEMY_TYPE_MAPPING = {
    # String type
    sa.String.__visit_name__: LLMTypeEnum.STR.value,
    sa.Text.__visit_name__: LLMTypeEnum.STR.value,
    sa.Unicode.__visit_name__: LLMTypeEnum.STR.value,
    sa.UnicodeText.__visit_name__: LLMTypeEnum.STR.value,
    sa.VARCHAR.__visit_name__: LLMTypeEnum.STR.value,
    sa.NVARCHAR.__visit_name__: LLMTypeEnum.STR.value,
    sa.CHAR.__visit_name__: LLMTypeEnum.STR.value,
    sa.NCHAR.__visit_name__: LLMTypeEnum.STR.value,
    sa.TEXT.__visit_name__: LLMTypeEnum.STR.value,
    sa.CLOB.__visit_name__: LLMTypeEnum.STR.value,
    # Integer type
    sa.Integer.__visit_name__: LLMTypeEnum.INT.value,
    sa.SmallInteger.__visit_name__: LLMTypeEnum.INT.value,
    sa.BigInteger.__visit_name__: LLMTypeEnum.INT.value,
    sa.INTEGER.__visit_name__: LLMTypeEnum.INT.value,
    sa.SMALLINT.__visit_name__: LLMTypeEnum.INT.value,
    sa.BIGINT.__visit_name__: LLMTypeEnum.INT.value,
    # float type
    sa.Float.__visit_name__: LLMTypeEnum.FLOAT.value,
    sa.Double.__visit_name__: LLMTypeEnum.FLOAT.value,
    sa.REAL.__visit_name__: LLMTypeEnum.FLOAT.value,
    sa.FLOAT.__visit_name__: LLMTypeEnum.FLOAT.value,
    sa.DOUBLE.__visit_name__: LLMTypeEnum.FLOAT.value,
    sa.DOUBLE_PRECISION.__visit_name__: LLMTypeEnum.FLOAT.value,
    # decimal type
    sa.Numeric.__visit_name__: LLMTypeEnum.DEC.value,
    sa.NUMERIC.__visit_name__: LLMTypeEnum.DEC.value,
    sa.DECIMAL.__visit_name__: LLMTypeEnum.DEC.value,
    # datetime
    sa.DateTime.__visit_name__: LLMTypeEnum.DT.value,
    sa.DATETIME.__visit_name__: LLMTypeEnum.DT.value,
    sa.TIMESTAMP.__visit_name__: LLMTypeEnum.TS.value,
    sa.Date.__visit_name__: LLMTypeEnum.DATE.value,
    sa.DATE.__visit_name__: LLMTypeEnum.DATE.value,
    sa.Time.__visit_name__: LLMTypeEnum.TIME.value,
    sa.TIME.__visit_name__: LLMTypeEnum.TIME.value,
    # binary type
    sa.LargeBinary.__visit_name__: LLMTypeEnum.BLOB.value,
    sa.BLOB.__visit_name__: LLMTypeEnum.BLOB.value,
    sa.BINARY.__visit_name__: LLMTypeEnum.BIN.value,
    sa.VARBINARY.__visit_name__: LLMTypeEnum.BIN.value,
    # bool type
    sa.Boolean.__visit_name__: LLMTypeEnum.BOOL.value,
    sa.BOOLEAN.__visit_name__: LLMTypeEnum.BOOL.value,
    # special types
    sa.Enum.__visit_name__: LLMTypeEnum.STR.value,  #  (stored as string)
    sa.JSON.__visit_name__: LLMTypeEnum.STR.value,
    sa.Uuid.__visit_name__: LLMTypeEnum.STR.value,  #  (default storage format)
    sa.UUID.__visit_name__: LLMTypeEnum.STR.value,
    sa.Null.__visit_name__: LLMTypeEnum.NULL.value,
    # Additional types not in original mapping
    sa.ARRAY.__visit_name__: LLMTypeEnum.STR.value,  #
    sa.TypeDecorator.__visit_name__: LLMTypeEnum.STR.value,  #  (PickleType, Interval, Variant)
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


def sqlalchemy_type_to_llm_type(type_: TypeEngine) -> str:
    """
    Create a ColumnType instance from a SQLAlchemy TypeEngine object.

    This method extracts type information from a SQLAlchemy type object and maps it
    to our simplified type system. It uses the type's visit_name attribute for mapping
    when available, falling back to the string representation for unknown types.

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
