# -*- coding: utf-8 -*-

import typing as T
import textwrap

from .server import mcp
from .hub.hub_init import hub


def get_description(method: T.Callable) -> str:
    """
    Get the description of a function, falling back to its docstring if available.
    """
    return textwrap.dedent(method.__doc__).strip()


@mcp.tool(
    description=get_description(hub.tool_list_databases),
)
async def list_databases() -> str:
    return hub.tool_list_databases()


@mcp.tool(
    description=get_description(hub.tool_list_tables),
)
async def list_tables(
    database_identifier: str,
    schema_name: T.Optional[str] = None,
) -> str:
    return hub.tool_list_tables(
        database_identifier=database_identifier,
        schema_name=schema_name,
    )


@mcp.tool(
    description=get_description(hub.tool_get_database_details),
)
async def get_database_details() -> str:
    return hub.tool_get_database_details()


@mcp.tool(
    description=get_description(hub.tool_get_schema_details),
)
async def get_schema_details(
    database_identifier: str,
    schema_name: T.Optional[str] = None,
) -> str:
    return hub.tool_get_schema_details(
        database_identifier=database_identifier,
        schema_name=schema_name,
    )


@mcp.tool(
    description=get_description(hub.tool_execute_select_statement),
)
async def execute_select_statement(
    database_identifier: str,
    sql: str,
    params: T.Optional[dict[str, T.Any]] = None,
) -> str:
    return hub.tool_execute_select_statement(
        database_identifier=database_identifier,
        sql=sql,
        params=params,
    )
