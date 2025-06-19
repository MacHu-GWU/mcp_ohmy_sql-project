# -*- coding: utf-8 -*-

import pytest

from which_runtime.api import runtime

from mcp_ohmy_sql.tests.test_config import DatabaseEnum


class TestToolAdapterMixin:
    def test_tool_list_databases(
        self,
        mcp_ohmy_sql_adapter,
    ):
        s = mcp_ohmy_sql_adapter.tool_list_databases()
        # print(s) # for debug only

    def test_tool_list_tables(
        self,
        mcp_ohmy_sql_adapter,
        sqlite_sa_engine_objs,
    ):
        s = mcp_ohmy_sql_adapter.tool_list_tables(
            database_identifier=DatabaseEnum.chinook_sqlite.identifier
        )
        # print(s) # for debug only

        s = mcp_ohmy_sql_adapter.tool_list_tables(
            database_identifier="invalid database"
        )
        assert "Database 'invalid database' not found in configuration" in s

    @pytest.mark.skipif(
        condition=runtime.is_local_runtime_group is False,
        reason="only run on local runtime",
    )
    def test_tool_list_tables_with_real_database(
        self,
        mcp_ohmy_sql_adapter,
        sqlite_sa_engine_objs,
    ):
        s = mcp_ohmy_sql_adapter.tool_list_tables(
            database_identifier=DatabaseEnum.chinook_redshift.identifier,
            schema_name=DatabaseEnum.chinook_redshift.schemas[0].name,
        )
        # print(s)

    def test_tool_get_all_database_details(
        self,
        mcp_ohmy_sql_adapter,
        sqlite_sa_engine_objs,
    ):
        s = mcp_ohmy_sql_adapter.tool_get_all_database_details()
        # print(s)  # for debug only

    def test_get_schema_details(
        self,
        mcp_ohmy_sql_adapter,
        sqlite_sa_engine_objs,
    ):
        s = mcp_ohmy_sql_adapter.tool_get_schema_details(
            database_identifier=DatabaseEnum.chinook_sqlite.identifier,
        )
        # print(s)  # for debug only

        s = mcp_ohmy_sql_adapter.tool_get_schema_details(
            database_identifier="invalid database",
        )
        assert "Database 'invalid database' not found in configuration" in s

    @pytest.mark.skipif(
        condition=runtime.is_local_runtime_group is False,
        reason="only run on local runtime",
    )
    def test_get_schema_details_with_real_database(
        self,
        mcp_ohmy_sql_adapter,
        sqlite_sa_engine_objs,
    ):
        s = mcp_ohmy_sql_adapter.tool_get_schema_details(
            database_identifier=DatabaseEnum.chinook_redshift.identifier,
            schema_name=DatabaseEnum.chinook_redshift.schemas[0].name,
        )
        # print(s)  # for debug only

    def test_tool_execute_select_statement(
        self,
        mcp_ohmy_sql_adapter,
        sqlite_sa_engine_objs,
    ):
        s = mcp_ohmy_sql_adapter.tool_execute_select_statement(
            database_identifier=DatabaseEnum.chinook_sqlite.identifier,
            sql="SELECT 1",
        )
        # print(s)  # for debug only

        s = mcp_ohmy_sql_adapter.tool_execute_select_statement(
            database_identifier="invalid database",
            sql="SELECT 1",
        )
        assert "Database 'invalid database' not found in configuration" in s

    @pytest.mark.skipif(
        condition=runtime.is_local_runtime_group is False,
        reason="only run on local runtime",
    )
    def test_tool_execute_select_statement_with_real_database(
        self,
        mcp_ohmy_sql_adapter,
        sqlite_sa_engine_objs,
    ):
        s = mcp_ohmy_sql_adapter.tool_execute_select_statement(
            database_identifier=DatabaseEnum.chinook_redshift.identifier,
            sql="SELECT 1",
        )
        # print(s)  # for debug only


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.adapter.tool_adapter.py",
        preview=False,
    )
