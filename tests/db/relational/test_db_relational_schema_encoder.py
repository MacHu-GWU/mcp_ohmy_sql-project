# -*- coding: utf-8 -*-

"""
Test module for mcp_ohmy_sql.db.relational.schema_encoder module.

This module contains comprehensive unit tests for the sqlalchemy_type_to_llm_type function
and the SQLALCHEMY_TYPE_MAPPING constant, covering all SQLAlchemy type mappings.
"""

import sqlalchemy as sa
from sqlalchemy.types import TypeEngine
from mcp_ohmy_sql.db.relational.schema_encoder import sqlalchemy_type_to_llm_type
from mcp_ohmy_sql.constants import LLMTypeEnum


def _test_sqlalchemy_type_to_llm_type(
    ith: int,
    sa_type: TypeEngine,
    llm_type: str,
    is_match: bool,
):
    if is_match:
        assert (
            sqlalchemy_type_to_llm_type(sa_type) == llm_type
        ), f"Test case {ith} failed: {sa_type} should map to {llm_type}"


def test_sqlalchemy_type_to_llm_type():
    cases = [
        # String/Text types - all character-based data types
        (sa.String(), LLMTypeEnum.STR.value, True),
        (sa.String(100), LLMTypeEnum.STR.value, True),
        (sa.Text(), LLMTypeEnum.STR.value, True),
        (sa.Unicode(), LLMTypeEnum.STR.value, True),
        (sa.UnicodeText(), LLMTypeEnum.STR.value, True),
        (sa.VARCHAR(255), LLMTypeEnum.STR.value, True),
        (sa.CHAR(10), LLMTypeEnum.STR.value, True),
        (sa.NVARCHAR(100), LLMTypeEnum.STR.value, True),
        (sa.NCHAR(10), LLMTypeEnum.STR.value, True),
        (sa.TEXT(), LLMTypeEnum.STR.value, True),
        (sa.CLOB(), LLMTypeEnum.STR.value, True),
        # Integer types - all whole number data types
        (sa.Integer(), LLMTypeEnum.INT.value, True),
        (sa.SmallInteger(), LLMTypeEnum.INT.value, True),
        (sa.BigInteger(), LLMTypeEnum.INT.value, True),
        (sa.INTEGER(), LLMTypeEnum.INT.value, True),
        (sa.SMALLINT(), LLMTypeEnum.INT.value, True),
        (sa.BIGINT(), LLMTypeEnum.INT.value, True),
        # Floating point types - all decimal number data types (approximate)
        (sa.Float(), LLMTypeEnum.FLOAT.value, True),
        (sa.Float(precision=24), LLMTypeEnum.FLOAT.value, True),
        (sa.Double(), LLMTypeEnum.FLOAT.value, True),
        (sa.REAL(), LLMTypeEnum.FLOAT.value, True),
        (sa.FLOAT(), LLMTypeEnum.FLOAT.value, True),
        (sa.DOUBLE(), LLMTypeEnum.FLOAT.value, True),
        (sa.DOUBLE_PRECISION(), LLMTypeEnum.FLOAT.value, True),
        # Decimal/Numeric types - exact precision decimal data types
        (sa.Numeric(), LLMTypeEnum.DEC.value, True),
        (sa.Numeric(10, 2), LLMTypeEnum.DEC.value, True),
        (sa.NUMERIC(10, 2), LLMTypeEnum.DEC.value, True),
        (sa.DECIMAL(10, 2), LLMTypeEnum.DEC.value, True),
        # DateTime types - date and time data types
        (sa.DateTime(), LLMTypeEnum.DT.value, True),
        (sa.DATETIME(), LLMTypeEnum.DT.value, True),
        # Timestamp types - timestamp with timezone awareness
        (sa.TIMESTAMP(), LLMTypeEnum.TS.value, True),
        # Date types - date only (no time component)
        (sa.Date(), LLMTypeEnum.DATE.value, True),
        (sa.DATE(), LLMTypeEnum.DATE.value, True),
        # Time types - time only (no date component)
        (sa.Time(), LLMTypeEnum.TIME.value, True),
        (sa.TIME(), LLMTypeEnum.TIME.value, True),
        # Binary Large Object types - for storing large binary data
        (sa.LargeBinary(), LLMTypeEnum.BLOB.value, True),
        (sa.LargeBinary(length=1024), LLMTypeEnum.BLOB.value, True),
        (sa.BLOB(), LLMTypeEnum.BLOB.value, True),
        # Binary types - for storing fixed or variable length binary data
        (sa.BINARY(), LLMTypeEnum.BIN.value, True),
        (sa.VARBINARY(), LLMTypeEnum.BIN.value, True),
        # Boolean types - true/false values
        (sa.Boolean(), LLMTypeEnum.BOOL.value, True),
        (sa.BOOLEAN(), LLMTypeEnum.BOOL.value, True),
        # Special types mapped to string - various specialized data types
        (sa.Enum("red", "green", "blue"), LLMTypeEnum.STR.value, True),
        (sa.JSON(), LLMTypeEnum.STR.value, True),
        (sa.Uuid(), LLMTypeEnum.STR.value, True),
        (sa.UUID(), LLMTypeEnum.STR.value, True),
        (sa.ARRAY(sa.Integer), LLMTypeEnum.STR.value, True),
        (sa.PickleType(), LLMTypeEnum.STR.value, True),
        (sa.Interval(), LLMTypeEnum.STR.value, True),
        # Null types - for columns that can only contain NULL
        (sa.Null(), LLMTypeEnum.NULL.value, True),
    ]

    for ith, (sa_type, llm_type, is_match) in enumerate(cases):
        _test_sqlalchemy_type_to_llm_type(ith, sa_type, llm_type, is_match)


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.db.relational.schema_encoder",
        preview=False,
    )
