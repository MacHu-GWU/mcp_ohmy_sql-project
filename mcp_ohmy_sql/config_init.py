# -*- coding: utf-8 -*-

from pathlib import Path

from .constants import EnvVarNameEnum
from .config import Config

FINAL_SQL_MCP_CONFIG = EnvVarNameEnum.FINAL_SQL_MCP_CONFIG.value
path_final_sql_mcp_config = Path(FINAL_SQL_MCP_CONFIG)
from .paths import path_config as path_final_sql_mcp_config

config = Config.load(path=path_final_sql_mcp_config)
