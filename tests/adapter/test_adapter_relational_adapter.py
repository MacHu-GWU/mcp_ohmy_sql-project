# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.test_config import DatabaseEnum

try:
    from rich import print as rprint
except ImportError:  # pragma: no cover
    pass


class TestRelationalAdapterMixin:
    def test_get_relational_schema_info(
        self,
        mcp_ohmy_sql_adapter,
    ):
        flag, msg, database, schema = mcp_ohmy_sql_adapter.get_database_and_schema_object(
            DatabaseEnum.chinook_sqlite.identifier,
        )
        schema_info = mcp_ohmy_sql_adapter.get_relational_schema_info(database, schema)
        # print(schema_info)  # for debug only

    def test_get_relational_database_info(
        self,
        mcp_ohmy_sql_config,
        mcp_ohmy_sql_adapter,
    ):
        flag, msg, database, schema = mcp_ohmy_sql_adapter.get_database_and_schema_object(
            DatabaseEnum.chinook_sqlite.identifier,
        )
        database_info = mcp_ohmy_sql_adapter.get_relational_database_info(database)
        # rprint(database_info)  # for debug only


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.adapter.relational_adapter.py",
        preview=False,
    )
