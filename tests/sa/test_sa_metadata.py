# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.config import config, chinook_db
from mcp_ohmy_sql.sa.metadata import SchemaInfo

from rich import print as rprint


class TestSchemaInfo:
    def test_from_metadata(self):
        schema_info = SchemaInfo.from_metadata(
            engine=chinook_db.sa_engine,
            metadata=chinook_db.sa_metadata,
            schema_name=chinook_db.schemas[0].name,
            exclude=[
                "Playlist",
                "PlaylistTrack",
            ],
        )
        # rprint(schema_info)
        # rprint(schema_info.tables_mapping)
        assert "Playlist" not in schema_info.tables_mapping
        assert "PlaylistTrack" not in schema_info.tables_mapping

        table_info = schema_info.tables[0]
        # rprint(table_info)
        # rprint(table_info.columns_mapping)

        column_info = table_info.columns[0]
        # rprint(column_info)


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.sa.metadata",
        preview=False,
    )
