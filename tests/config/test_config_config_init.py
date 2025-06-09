# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.config import config

from rich import print as rprint


def test_config_init():
    rprint(config)  # for debug only
    pass


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_unit_test

    run_unit_test(__file__)
