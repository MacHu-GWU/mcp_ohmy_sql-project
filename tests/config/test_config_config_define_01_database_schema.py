# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.config import config

from rich import print as rprint


class TestConfigDatabaseSchemaMixin:
    def test_get_database_schema(self):
        print("")
        s = config.get_database_schema()
        print(s)  # for debug only


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.config.config_define_01_database_schema.py",
        preview=False,
    )
