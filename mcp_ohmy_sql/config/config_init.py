# -*- coding: utf-8 -*-

import os
from pathlib import Path

from which_runtime.api import runtime

from ..constants import EnvVarEnum

from .config_define_00_main import Config

if (
    "READTHEDOCS" in os.environ
): # pragma: no cover
    from ..paths import path_sample_config
    MCP_OHMY_SQL_CONFIG = str(path_sample_config)
else:
    MCP_OHMY_SQL_CONFIG = EnvVarEnum.MCP_OHMY_SQL_CONFIG.value

print(f"{MCP_OHMY_SQL_CONFIG = }")
path_mcp_ohmy_sql_config = Path(MCP_OHMY_SQL_CONFIG)
config = Config.load(path=path_mcp_ohmy_sql_config)
