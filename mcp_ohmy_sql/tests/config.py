# -*- coding: utf-8 -*-

import os

from . import chinook

from ..paths import path_config
from ..constants import EnvVarEnum

os.environ[EnvVarEnum.MCP_OHMY_SQL_CONFIG.name] = str(path_config)

from ..config.config_init import config

chinook_db = config.databases_mapping["chinook"]
