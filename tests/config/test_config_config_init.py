# -*- coding: utf-8 -*-

import os

from mcp_ohmy_sql.paths import path_sample_config
from mcp_ohmy_sql.constants import EnvVarEnum

os.environ[EnvVarEnum.MCP_OHMY_SQL_CONFIG.name] = str(path_sample_config)

from mcp_ohmy_sql.config.config_init import config

try:
    from rich import print as rprint
except ImportError:  # pragma: no cover
    pass


def test_config_init():
    _ = config
    # rprint(config)  # for debug only
    pass


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.config.config_init.py",
        preview=False,
    )
