# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.config import config, DatabaseEnum

from rich import print as rprint


def setup_module(module):
    print("")


class TestConfigDatabaseSchemaMixin:
    def test_get_schema_object(self):
        flag, msg, database, schema = config.get_schema_object("invalid database")
        assert flag is False
        assert "Error: Database" in msg

        flag, msg, database, schema = config.get_schema_object(
            DatabaseEnum.chinook_sqlite.identifier, "invalid schema"
        )
        assert flag is False
        assert "Error: Schema" in msg

    def test_get_schema_info(self):
        flag, msg, database, schema = config.get_schema_object(
            DatabaseEnum.chinook_sqlite.identifier,
        )
        schema_info = config.get_schema_info(database, schema)
        # print(schema_info)  # for debug only

    def test_get_database_schema(self):
        s = config.get_database_schema()
        # print(s)  # for debug only


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.config.config_define_01_database_schema.py",
        preview=False,
    )
