# -*- coding: utf-8 -*-

import os

from ..paths import path_config
from ..constants import EnvVarEnum

from .test_database_setup import DBUrlEnum

os.environ[EnvVarEnum.MCP_OHMY_SQL_CONFIG.name] = str(path_config)

from ..config.config_init import config

chinook_sqlite = config.databases_mapping["chinook sqlite"]
chinook_sqlite.connection.create_engine_kwargs = {"url": DBUrlEnum.sqlite}
chinook_psql = config.databases_mapping["chinook postgres"]
