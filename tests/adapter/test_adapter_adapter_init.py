# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.test_config_1_define import setup_test_config

setup_test_config()

from mcp_ohmy_sql.adapter.adapter_init import adapter

try:
    from rich import print as rprint
except ImportError:  # pragma: no cover
    pass


def test_config_init():
    _ = adapter
    # rprint(adapter)  # for debug only
    pass


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.adapter.adapter_init.py",
        preview=False,
    )
