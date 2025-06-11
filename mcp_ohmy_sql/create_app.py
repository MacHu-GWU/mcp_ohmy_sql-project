# -*- coding: utf-8 -*-


def create_app():
    from .server import mcp

    from .tools import list_databases
    from .tools import list_tables
    from .tools import get_database_details
    from .tools import get_schema_details
    from .tools import execute_select_statement

    return mcp
