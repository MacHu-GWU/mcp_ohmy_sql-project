# -*- coding: utf-8 -*-

from mcp_ohmy_sql.constants import (
    DbTypeEnum,
    TableTypeEnum,
    LLMColumnConstraintEnum,
    LLMTypeEnum,
)
from mcp_ohmy_sql.db.relational.schema_2_encoder import (
    encode_column_info,
    encode_table_info,
    encode_schema_info,
    encode_database_info,
)
from mcp_ohmy_sql.tests.chinook.chinook_data_model import (
    ChinookTableNameEnum,
    ChinookViewNameEnum,
    Artist,
    Album,
)


def test_encode_column_info(
    in_memory_sqlite_sa_schema_info_objects,
):
    schema_info_objects = in_memory_sqlite_sa_schema_info_objects

    s = encode_column_info(
        table_info=schema_info_objects.t_album_info,
        column_info=schema_info_objects.c_album_album_id_info,
    )
    expected = f"{Album.AlbumId.name}:{LLMTypeEnum.INT.value}*{LLMColumnConstraintEnum.PK.value}"
    assert s == expected

    s = encode_column_info(
        table_info=schema_info_objects.t_album_info,
        column_info=schema_info_objects.c_album_artist_id_info,
    )
    expected = f"{Album.ArtistId.name}:{LLMTypeEnum.INT.value}*{LLMColumnConstraintEnum.NN.value}*{LLMColumnConstraintEnum.FK.value}->{ChinookTableNameEnum.Artist.value}.{Artist.ArtistId.name}"
    assert s == expected

    s = encode_column_info(
        table_info=schema_info_objects.t_album_info,
        column_info=schema_info_objects.c_album_title_id_info,
    )
    expected = (
        f"{Album.Title.name}:{LLMTypeEnum.STR.value}*{LLMColumnConstraintEnum.NN.value}"
    )
    assert s == expected


def test_encode_table_info(
    in_memory_sqlite_sa_schema_info_objects,
):
    schema_info_objects = in_memory_sqlite_sa_schema_info_objects

    s = encode_table_info(table_info=schema_info_objects.t_album_info)
    expected = f"""
{TableTypeEnum.TABLE.value} {ChinookTableNameEnum.Album.value}(
  {Album.AlbumId.name}:{LLMTypeEnum.INT.value}*{LLMColumnConstraintEnum.PK.value},
  {Album.Title.name}:{LLMTypeEnum.STR.value}*{LLMColumnConstraintEnum.NN.value},
  {Album.ArtistId.name}:{LLMTypeEnum.INT.value}*{LLMColumnConstraintEnum.NN.value}*{LLMColumnConstraintEnum.FK.value}->{ChinookTableNameEnum.Artist.value}.{Artist.ArtistId.name},
)
""".strip()
    assert s == expected

    s = encode_table_info(table_info=schema_info_objects.v_album_sales_stats_info)
    expected = f"""
{TableTypeEnum.VIEW.value} {ChinookViewNameEnum.AlbumSalesStats.value}(
  AlbumId:{LLMTypeEnum.INT.value},
  AlbumTitle:{LLMTypeEnum.STR.value},
  ArtistName:{LLMTypeEnum.STR.value},
  TotalSales:{LLMTypeEnum.INT.value},
  TotalQuantity:{LLMTypeEnum.INT.value},
  TotalRevenue:{LLMTypeEnum.DEC.value},
  AvgTrackPrice:{LLMTypeEnum.DEC.value},
  TracksInAlbum:{LLMTypeEnum.INT.value},
)
""".strip()
    assert s == expected


def test_encode_schema_info(
    in_memory_sqlite_sa_schema_info_objects,
):
    schema_info_objects = in_memory_sqlite_sa_schema_info_objects

    s = encode_schema_info(schema_info=schema_info_objects.schema_info)
    # print(s)  # for debugging only
    assert s.startswith(f"Schema default")


def test_encode_database_info(
    in_memory_sqlite_sa_schema_info_objects,
):
    schema_info_objects = in_memory_sqlite_sa_schema_info_objects
    database_info = schema_info_objects.database_info

    s = encode_database_info(database_info=database_info)
    # print(s)  # for debugging only
    assert s.startswith(f"{DbTypeEnum.SQLITE.value} Database {database_info.name}")


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.db.relational.schema_2_encoder",
        preview=False,
    )
