# -*- coding: utf-8 -*-

"""
This script sets up a test configuration for testing purposes.
"""

import os

from which_runtime.api import runtime

from ..paths import path_sample_config
from ..constants import EnvVarEnum

os.environ[EnvVarEnum.MCP_OHMY_SQL_CONFIG.name] = str(path_sample_config)

from .test_config import DatabaseEnum, config
from .test_database_setup import setup_test_database

if runtime.is_ci_runtime_group:
    setup_test_database(engine=DatabaseEnum.chinook_sqlite.sa_engine)
