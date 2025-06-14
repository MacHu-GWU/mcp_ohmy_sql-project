# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy.types import TypeEngine

from mcp_ohmy_sql.constants import ObjectTypeEnum, LLMTypeEnum, DbTypeEnum

from mcp_ohmy_sql.db.relational.schema_extractor import (
    sqlalchemy_type_to_llm_type,
    new_foreign_key_info,
    new_column_info,
    new_table_info,
    new_schema_info,
    new_database_info,
)

from mcp_ohmy_sql.tests.chinook.chinook_data_model import (
    ChinookTableNameEnum,
    ChinookViewNameEnum,
    Base,
    Artist,
    Album,
    album_sales_stats_view_select_stmt,
)


def _test_sqlalchemy_type_to_llm_type(
    ith: int,
    sa_type: TypeEngine,
    llm_type: LLMTypeEnum,
    is_match: bool,
):
    if is_match:
        assert (
            sqlalchemy_type_to_llm_type(sa_type) is llm_type
        ), f"Test case {ith} failed: {sa_type} should map to {llm_type}"


def test_sqlalchemy_type_to_llm_type():
    cases = [
        # String/Text types - all character-based data types
        (sa.String(), LLMTypeEnum.STR, True),
        (sa.String(100), LLMTypeEnum.STR, True),
        (sa.Text(), LLMTypeEnum.STR, True),
        (sa.Unicode(), LLMTypeEnum.STR, True),
        (sa.UnicodeText(), LLMTypeEnum.STR, True),
        (sa.VARCHAR(255), LLMTypeEnum.STR, True),
        (sa.CHAR(10), LLMTypeEnum.STR, True),
        (sa.NVARCHAR(100), LLMTypeEnum.STR, True),
        (sa.NCHAR(10), LLMTypeEnum.STR, True),
        (sa.TEXT(), LLMTypeEnum.STR, True),
        (sa.CLOB(), LLMTypeEnum.STR, True),
        # Integer types - all whole number data types
        (sa.Integer(), LLMTypeEnum.INT, True),
        (sa.SmallInteger(), LLMTypeEnum.INT, True),
        (sa.BigInteger(), LLMTypeEnum.INT, True),
        (sa.INTEGER(), LLMTypeEnum.INT, True),
        (sa.SMALLINT(), LLMTypeEnum.INT, True),
        (sa.BIGINT(), LLMTypeEnum.INT, True),
        # Floating point types - all decimal number data types (approximate)
        (sa.Float(), LLMTypeEnum.FLOAT, True),
        (sa.Float(precision=24), LLMTypeEnum.FLOAT, True),
        (sa.Double(), LLMTypeEnum.FLOAT, True),
        (sa.REAL(), LLMTypeEnum.FLOAT, True),
        (sa.FLOAT(), LLMTypeEnum.FLOAT, True),
        (sa.DOUBLE(), LLMTypeEnum.FLOAT, True),
        (sa.DOUBLE_PRECISION(), LLMTypeEnum.FLOAT, True),
        # Decimal/Numeric types - exact precision decimal data types
        (sa.Numeric(), LLMTypeEnum.DEC, True),
        (sa.Numeric(10, 2), LLMTypeEnum.DEC, True),
        (sa.NUMERIC(10, 2), LLMTypeEnum.DEC, True),
        (sa.DECIMAL(10, 2), LLMTypeEnum.DEC, True),
        # DateTime types - date and time data types
        (sa.DateTime(), LLMTypeEnum.DT, True),
        (sa.DATETIME(), LLMTypeEnum.DT, True),
        # Timestamp types - timestamp with timezone awareness
        (sa.TIMESTAMP(), LLMTypeEnum.TS, True),
        # Date types - date only (no time component)
        (sa.Date(), LLMTypeEnum.DATE, True),
        (sa.DATE(), LLMTypeEnum.DATE, True),
        # Time types - time only (no date component)
        (sa.Time(), LLMTypeEnum.TIME, True),
        (sa.TIME(), LLMTypeEnum.TIME, True),
        # Binary Large Object types - for storing large binary data
        (sa.LargeBinary(), LLMTypeEnum.BLOB, True),
        (sa.LargeBinary(length=1024), LLMTypeEnum.BLOB, True),
        (sa.BLOB(), LLMTypeEnum.BLOB, True),
        # Binary types - for storing fixed or variable length binary data
        (sa.BINARY(), LLMTypeEnum.BIN, True),
        (sa.VARBINARY(), LLMTypeEnum.BIN, True),
        # Boolean types - true/false values
        (sa.Boolean(), LLMTypeEnum.BOOL, True),
        (sa.BOOLEAN(), LLMTypeEnum.BOOL, True),
        # Special types mapped to string - various specialized data types
        (sa.Enum("red", "green", "blue"), LLMTypeEnum.STR, True),
        (sa.JSON(), LLMTypeEnum.STR, True),
        (sa.Uuid(), LLMTypeEnum.STR, True),
        (sa.UUID(), LLMTypeEnum.STR, True),
        (sa.ARRAY(sa.Integer), LLMTypeEnum.STR, True),
        (sa.PickleType(), LLMTypeEnum.STR, True),
        (sa.Interval(), LLMTypeEnum.STR, True),
        # Null types - for columns that can only contain NULL
        (sa.Null(), LLMTypeEnum.NULL, True),
    ]

    for ith, (sa_type, llm_type, is_match) in enumerate(cases):
        _test_sqlalchemy_type_to_llm_type(ith, sa_type, llm_type, is_match)


def test_new_foreign_key_info(
    in_memory_sqlite_sa_objects,
):
    sa_objs = in_memory_sqlite_sa_objects
    fk_albumn_artist_id_info = new_foreign_key_info(sa_objs.fk_album_artist_id)
    assert fk_albumn_artist_id_info.object_type is ObjectTypeEnum.FOREIGN_KEY
    assert (
        fk_albumn_artist_id_info.name
        == f"{ChinookTableNameEnum.Artist.value}.{Artist.ArtistId.name}"
    )


def test_new_column_info(
    in_memory_sqlite_sa_objects,
):
    sa_objs = in_memory_sqlite_sa_objects

    c_album_album_id_info = new_column_info(
        table=sa_objs.t_album,
        column=sa_objs.c_album_album_id,
    )
    assert c_album_album_id_info.llm_type is LLMTypeEnum.INT
    assert c_album_album_id_info.primary_key is True
    assert c_album_album_id_info.nullable is False

    c_album_title_id_info = new_column_info(
        table=sa_objs.t_album,
        column=sa_objs.c_album_title_id,
    )
    assert c_album_title_id_info.llm_type is LLMTypeEnum.STR
    assert c_album_title_id_info.primary_key is False
    assert c_album_title_id_info.nullable is False

    c_album_artist_id_info = new_column_info(
        table=sa_objs.t_album,
        column=sa_objs.c_album_artist_id,
    )
    assert c_album_artist_id_info.object_type is ObjectTypeEnum.COLUMN
    assert c_album_artist_id_info.llm_type is LLMTypeEnum.INT
    assert c_album_artist_id_info.primary_key is False
    assert c_album_artist_id_info.nullable is False


def test_new_table_info(
    in_memory_sqlite_sa_objects,
):
    sa_objs = in_memory_sqlite_sa_objects

    t_album_info = new_table_info(
        table=sa_objs.t_album,
        object_type=ObjectTypeEnum.TABLE,
    )
    assert t_album_info.object_type is ObjectTypeEnum.TABLE
    assert t_album_info.name == ChinookTableNameEnum.Album.value
    assert t_album_info.fullname == ChinookTableNameEnum.Album.value
    assert len(t_album_info.primary_key) == 1
    assert len(t_album_info.foreign_keys) == 1
    assert len(t_album_info.columns) == 3


def _test_new_schema_info_and_new_database_info(
    engine: sa.engine.Engine,
    metadata: sa.MetaData,
):
    schema_info = new_schema_info(
        engine=engine,
        metadata=metadata,
        schema_name=None,
        exclude=["PlaylistTrack", "Playlist"],
    )
    assert schema_info.object_type is ObjectTypeEnum.SCHEMA

    view = schema_info.tables_mapping[ChinookViewNameEnum.AlbumSalesStats.value]
    assert view.object_type is ObjectTypeEnum.VIEW

    database_info = new_database_info(
        name="Chinook",
        db_type=DbTypeEnum.SQLITE,
        schemas=[schema_info],
    )
    assert database_info.object_type is ObjectTypeEnum.DATABASE


def test_new_schema_info_and_new_database_info_1st(
    in_memory_sqlite_engine_objs,
):
    _test_new_schema_info_and_new_database_info(
        in_memory_sqlite_engine_objs.engine,
        in_memory_sqlite_engine_objs.metadata,
    )


def test_new_schema_info_and_new_database_info_2nd(
    in_memory_sqlite_engine_objs,
):
    _test_new_schema_info_and_new_database_info(
        in_memory_sqlite_engine_objs.engine,
        in_memory_sqlite_engine_objs.metadata,
    )


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.db.relational.schema_extractor",
        preview=False,
    )
