# -*- coding: utf-8 -*-


def create_app():
    from .server import mcp
    from .tools import get_database_schema_info

    return mcp
