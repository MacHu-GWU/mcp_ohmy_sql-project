# -*- coding: utf-8 -*-

import os

from . import chinook

from ..paths import path_config, path_chinook_sqlite
from ..constants import EnvVarEnum

os.environ[EnvVarEnum.MCP_OHMY_SQL_CONFIG.name] = str(path_config)

from ..config.config_init import config

chinook_db = config.databases_mapping["chinook"]
chinook_db.connection.create_engine_kwargs = {"url": f"sqlite:///{path_chinook_sqlite}"}
