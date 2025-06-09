# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.config import config, chinook_sqlite, chinook_psql

sqlite_engine = chinook_sqlite.sa_engine
sqlite_metadata = chinook_sqlite.sa_metadata
psql_engine = chinook_psql.sa_engine
