# -*- coding: utf-8 -*-

from pathlib import Path

from ..constants import EnvVarEnum

from .config_define_00_main import Config

MCP_OHMY_SQL_CONFIG = EnvVarEnum.MCP_OHMY_SQL_CONFIG.value
path_mcp_ohmy_sql_config = Path(MCP_OHMY_SQL_CONFIG)
config = Config.load(path=path_mcp_ohmy_sql_config)
