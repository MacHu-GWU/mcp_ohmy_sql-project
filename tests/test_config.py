# -*- coding: utf-8 -*-

from mcp_ohmy_sql.config import Config
from mcp_ohmy_sql.paths import path_config


def test():
    config = Config.load(path_config)
    _ = config.metadata


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.config",
        preview=False,
    )
