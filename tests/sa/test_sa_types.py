# -*- coding: utf-8 -*-

"""
Test module for mcp_ohmy_sql.sa.types module.

This module contains comprehensive unit tests for the ColumnType class and its
from_type() method, covering all SQLAlchemy type mappings.
"""

from sqlalchemy import types as sqltypes

from mcp_ohmy_sql.sa.types import ColumnType, SQLALCHEMY_TYPE_MAPPING
from mcp_ohmy_sql.constants import (
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


class TestColumnType:
    """Test cases for the ColumnType class."""

    def test_column_type_creation(self):
        """Test basic ColumnType instance creation."""
        ct = ColumnType(name="VARCHAR(50)", llm_name="STR")
        assert ct.name == "VARCHAR(50)"
        assert ct.llm_name == "STR"

    def test_from_type_string_types(self):
        """Test from_type() method with string/text types."""
        # Generic string types
        ct = ColumnType.from_type(sqltypes.String())
        assert ct.llm_name == STR
        assert "String" in ct.name or "VARCHAR" in ct.name

        ct = ColumnType.from_type(sqltypes.String(100))
        assert ct.llm_name == STR

        ct = ColumnType.from_type(sqltypes.Text())
        assert ct.llm_name == STR

        ct = ColumnType.from_type(sqltypes.Unicode())
        assert ct.llm_name == STR

        ct = ColumnType.from_type(sqltypes.UnicodeText())
        assert ct.llm_name == STR

        # SQL standard string types
        ct = ColumnType.from_type(sqltypes.VARCHAR(255))
        assert ct.llm_name == STR
        assert "VARCHAR" in ct.name

        ct = ColumnType.from_type(sqltypes.CHAR(10))
        assert ct.llm_name == STR
        assert "CHAR" in ct.name

        ct = ColumnType.from_type(sqltypes.NVARCHAR(100))
        assert ct.llm_name == STR

        ct = ColumnType.from_type(sqltypes.NCHAR(10))
        assert ct.llm_name == STR

        ct = ColumnType.from_type(sqltypes.TEXT())
        assert ct.llm_name == STR

        ct = ColumnType.from_type(sqltypes.CLOB())
        assert ct.llm_name == STR

    def test_from_type_integer_types(self):
        """Test from_type() method with integer types."""
        # Generic integer types
        ct = ColumnType.from_type(sqltypes.Integer())
        assert ct.llm_name == INT

        ct = ColumnType.from_type(sqltypes.SmallInteger())
        assert ct.llm_name == INT

        ct = ColumnType.from_type(sqltypes.BigInteger())
        assert ct.llm_name == INT

        # SQL standard integer types
        ct = ColumnType.from_type(sqltypes.INTEGER())
        assert ct.llm_name == INT

        ct = ColumnType.from_type(sqltypes.SMALLINT())
        assert ct.llm_name == INT

        ct = ColumnType.from_type(sqltypes.BIGINT())
        assert ct.llm_name == INT

    def test_from_type_float_types(self):
        """Test from_type() method with floating point types."""
        # Generic float types
        ct = ColumnType.from_type(sqltypes.Float())
        assert ct.llm_name == FLOAT

        ct = ColumnType.from_type(sqltypes.Float(precision=24))
        assert ct.llm_name == FLOAT

        ct = ColumnType.from_type(sqltypes.Double())
        assert ct.llm_name == FLOAT

        # SQL standard float types
        ct = ColumnType.from_type(sqltypes.REAL())
        assert ct.llm_name == FLOAT

        ct = ColumnType.from_type(sqltypes.FLOAT())
        assert ct.llm_name == FLOAT

        ct = ColumnType.from_type(sqltypes.DOUBLE())
        assert ct.llm_name == FLOAT

        ct = ColumnType.from_type(sqltypes.DOUBLE_PRECISION())
        assert ct.llm_name == FLOAT

    def test_from_type_decimal_types(self):
        """Test from_type() method with decimal/numeric types."""
        # Generic decimal types
        ct = ColumnType.from_type(sqltypes.Numeric())
        assert ct.llm_name == DEC

        ct = ColumnType.from_type(sqltypes.Numeric(10, 2))
        assert ct.llm_name == DEC

        # SQL standard decimal types
        ct = ColumnType.from_type(sqltypes.NUMERIC(10, 2))
        assert ct.llm_name == DEC

        ct = ColumnType.from_type(sqltypes.DECIMAL(10, 2))
        assert ct.llm_name == DEC

    def test_from_type_datetime_types(self):
        """Test from_type() method with date/time types."""
        # DateTime types
        ct = ColumnType.from_type(sqltypes.DateTime())
        assert ct.llm_name == DT

        ct = ColumnType.from_type(sqltypes.DATETIME())
        assert ct.llm_name == DT

        # Timestamp type
        ct = ColumnType.from_type(sqltypes.TIMESTAMP())
        assert ct.llm_name == TS

        # Date types
        ct = ColumnType.from_type(sqltypes.Date())
        assert ct.llm_name == DATE

        ct = ColumnType.from_type(sqltypes.DATE())
        assert ct.llm_name == DATE

        # Time types
        ct = ColumnType.from_type(sqltypes.Time())
        assert ct.llm_name == TIME

        ct = ColumnType.from_type(sqltypes.TIME())
        assert ct.llm_name == TIME

    def test_from_type_binary_types(self):
        """Test from_type() method with binary types."""
        # LargeBinary type
        ct = ColumnType.from_type(sqltypes.LargeBinary())
        assert ct.llm_name == BLOB

        ct = ColumnType.from_type(sqltypes.LargeBinary(length=1024))
        assert ct.llm_name == BLOB

        # SQL standard binary types
        ct = ColumnType.from_type(sqltypes.BLOB())
        assert ct.llm_name == BLOB

        ct = ColumnType.from_type(sqltypes.BINARY())
        assert ct.llm_name == BIN

        ct = ColumnType.from_type(sqltypes.VARBINARY())
        assert ct.llm_name == BIN

    def test_from_type_boolean_type(self):
        """Test from_type() method with boolean types."""
        ct = ColumnType.from_type(sqltypes.Boolean())
        assert ct.llm_name == BOOL

        ct = ColumnType.from_type(sqltypes.BOOLEAN())
        assert ct.llm_name == BOOL

    def test_from_type_special_types(self):
        """Test from_type() method with special types."""
        # Enum type
        ct = ColumnType.from_type(sqltypes.Enum("red", "green", "blue"))
        assert ct.llm_name == STR

        # JSON type
        ct = ColumnType.from_type(sqltypes.JSON())
        assert ct.llm_name == STR

        # UUID types
        ct = ColumnType.from_type(sqltypes.Uuid())
        assert ct.llm_name == STR

        ct = ColumnType.from_type(sqltypes.UUID())
        assert ct.llm_name == STR

        # NullType
        ct = ColumnType.from_type(sqltypes.NullType())
        assert ct.llm_name == NULL

        # ARRAY type
        ct = ColumnType.from_type(sqltypes.ARRAY(sqltypes.Integer))
        assert ct.llm_name == STR

    def test_from_type_decorator_types(self):
        """Test from_type() method with TypeDecorator-based types."""
        # PickleType
        ct = ColumnType.from_type(sqltypes.PickleType())
        assert ct.llm_name == STR

        # Interval
        ct = ColumnType.from_type(sqltypes.Interval())
        assert ct.llm_name == STR

    def test_from_type_unknown_type(self):
        """Test from_type() method with unknown/custom types."""

        # Create a custom type without a visit_name
        class CustomType(sqltypes.TypeEngine):
            pass

        ct = ColumnType.from_type(CustomType())
        # Should fallback to string representation
        assert ct.llm_name == str(CustomType())
        assert "CustomType" in ct.name

    def test_from_type_with_parameters(self):
        """Test that from_type() preserves type parameters in the name."""
        ct = ColumnType.from_type(sqltypes.String(50))
        assert "50" in ct.name
        assert ct.llm_name == STR

        ct = ColumnType.from_type(sqltypes.DECIMAL(10, 2))
        assert "10" in ct.name and "2" in ct.name
        assert ct.llm_name == DEC

        ct = ColumnType.from_type(sqltypes.Float(precision=24))
        assert ct.llm_name == FLOAT

    def test_type_mapping_completeness(self):
        """Verify that our type mapping covers all expected SQLAlchemy types."""
        # List of all expected visit names based on SQLAlchemy types
        expected_visit_names = {
            # String types
            "string",
            "text",
            "unicode",
            "unicode_text",
            "VARCHAR",
            "NVARCHAR",
            "CHAR",
            "NCHAR",
            "TEXT",
            "CLOB",
            # Integer types
            "integer",
            "small_integer",
            "big_integer",
            "INTEGER",
            "SMALLINT",
            "BIGINT",
            # Float types
            "float",
            "double",
            "REAL",
            "FLOAT",
            "DOUBLE",
            "DOUBLE_PRECISION",
            # Decimal types
            "numeric",
            "NUMERIC",
            "DECIMAL",
            # DateTime types
            "datetime",
            "DATETIME",
            "TIMESTAMP",
            "date",
            "DATE",
            "time",
            "TIME",
            # Binary types
            "large_binary",
            "BLOB",
            "BINARY",
            "VARBINARY",
            # Boolean type
            "boolean",
            "BOOLEAN",
            # Special types
            "enum",
            "JSON",
            "uuid",
            "UUID",
            "null",
            "ARRAY",
            "type_decorator",
            "user_defined",
        }

        # Verify all expected types are in our mapping
        for visit_name in expected_visit_names:
            assert (
                visit_name in SQLALCHEMY_TYPE_MAPPING
            ), f"Missing mapping for {visit_name}"

    def test_all_mapped_types_have_valid_constants(self):
        """Verify that all mapped types use valid LLM type constants."""
        valid_constants = {
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
        }

        for visit_name, llm_type in SQLALCHEMY_TYPE_MAPPING.items():
            assert (
                llm_type in valid_constants
            ), f"Invalid constant {llm_type} for {visit_name}"


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.sa.types",
        preview=False,
    )
