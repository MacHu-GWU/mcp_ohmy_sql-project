# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.test_database_setup import DatabaseEnum, setup_test_database

# setup_test_database(engine=DatabaseEnum.sqlite)
setup_test_database(engine=DatabaseEnum.postgres)
