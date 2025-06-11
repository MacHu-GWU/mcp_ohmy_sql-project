# -*- coding: utf-8 -*-

import textwrap

from mcp_ohmy_sql.tests.test_config_init import config, DatabaseEnum
from mcp_ohmy_sql.sa.metadata import SchemaInfo
from mcp_ohmy_sql.sa.schema_encoder import (
    encode_column_info,
    encode_table_info,
    encode_schema_info,
)

from rich import print as rprint


def setup_module(module):
    print("")


def test_encode_column_info():
    database = DatabaseEnum.chinook_sqlite

    schema_info = SchemaInfo.from_metadata(
        engine=database.sa_engine,
        metadata=database.sa_metadata,
        schema_name=database.schemas[0].name,
        exclude=[
            "Playlist",
            "PlaylistTrack",
        ],
    )
    # rprint(schema_info) # for debug only
    table_info = schema_info.tables[0]
    # rprint(table_info) # for debug only
    column_info = table_info.columns[0]
    # rprint(column_info) # for debug only

    s = encode_column_info(table_info, column_info)
    # print(s) # for debug only
    expected = "AlbumId:INT*PK*NN"
    assert s == expected

    s = encode_table_info(table_info)
    # print(s)  # for debug only
    expected = textwrap.dedent(
        """
    Table Album(
      AlbumId:INT*PK*NN,
      Title:STR*NN,
      ArtistId:INT*NN*FK->Artist.ArtistId,
    )
    """
    ).strip()
    assert s == expected

    s = encode_schema_info(schema_info)
    # print(s)  # for debug only
    expected = textwrap.dedent(
        """
    Schema default(
      Table Album(
        AlbumId:INT*PK*NN,
        Title:STR*NN,
        ArtistId:INT*NN*FK->Artist.ArtistId,
      )
      Table Artist(
        ArtistId:INT*PK*NN,
        Name:STR,
      )
        """
    ).strip()
    assert s.startswith(expected)


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.sa.schema_encoder",
        preview=False,
    )
