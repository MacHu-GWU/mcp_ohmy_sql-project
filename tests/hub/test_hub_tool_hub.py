# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.test_config_init import DatabaseEnum
from mcp_ohmy_sql.tests.test_hub_init import hub


def test_tool_list_databases():
    s = hub.tool_list_databases()
    print(s)


def test_tool_list_tables():
    s = hub.tool_list_tables(database_identifier=DatabaseEnum.chinook_sqlite.identifier)
    # print(s)

    s = hub.tool_list_tables(database_identifier="invalid database")
    assert "Database 'invalid database' not found in configuration" in s


def test_tool_get_database_details():
    s = hub.tool_get_database_details()
    # print(s)


def test_get_schema_details():
    s = hub.tool_get_schema_details(
        database_identifier=DatabaseEnum.chinook_sqlite.identifier,
    )
    # print(s)

    s = hub.tool_get_schema_details(
        database_identifier="invalid database",
    )
    assert "Database 'invalid database' not found in configuration" in s


def test_tool_execute_select_statement():
    s = hub.tool_execute_select_statement(
        database_identifier=DatabaseEnum.chinook_sqlite.identifier,
        sql="SELECT 1",
    )
    # print(s)

    s = hub.tool_execute_select_statement(
        database_identifier="invalid database",
        sql="SELECT 1",
    )
    assert "Database 'invalid database' not found in configuration" in s


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.hub.tool_hub.py",
        preview=False,
    )
