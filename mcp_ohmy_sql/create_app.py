# -*- coding: utf-8 -*-


def create_app():
    from .server import mcp

    from .tools import get_database_schema
    from .tools import execute_select_statement

    return mcp
