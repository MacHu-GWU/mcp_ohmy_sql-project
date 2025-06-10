# -*- coding: utf-8 -*-

import pytest
from mcp_ohmy_sql.tests.config import config
from mcp_ohmy_sql.tools import (
    get_database_schema_details,
    list_databases,
    list_tables,
    get_schema_details,
    execute_select_statement,
)


@pytest.mark.asyncio
async def test_get_database_schema_details():
    s = await get_database_schema_details()
    # print(s)


@pytest.mark.asyncio
async def test_list_databases():
    s = await list_databases()
    # print(s)


@pytest.mark.asyncio
async def test_list_tables():
    s = await list_tables(
        database_identifier="chinook sqlite",
    )
    # print(s)


@pytest.mark.asyncio
async def test_get_schema_details():
    s = await get_schema_details(
        database_identifier="chinook sqlite",
    )
    # print(s)


@pytest.mark.asyncio
async def test_execute_select_statement():
    s = await execute_select_statement(
        database_identifier="chinook sqlite",
        sql="SELECT 1;",
    )
    # print(s)


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.tools",
        preview=False,
    )
