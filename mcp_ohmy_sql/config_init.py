# -*- coding: utf-8 -*-

from pathlib import Path

from .constants import EnvVarNameEnum
from .config import Config

MCP_OHMY_SQL_CONFIG = EnvVarNameEnum.MCP_OHMY_SQL_CONFIG.value
path_mcp_ohmy_sql_config = Path(MCP_OHMY_SQL_CONFIG)
# from .paths import path_config as path_mcp_ohmy_sql_config

config = Config.load(path=path_mcp_ohmy_sql_config)
