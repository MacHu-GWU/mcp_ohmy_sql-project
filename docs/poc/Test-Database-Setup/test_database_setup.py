# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.test_database_setup import EngineEnum, setup_test_database

setup_test_database(engine=EngineEnum.sqlite)
# setup_test_database(engine=EngineEnum.postgres)
