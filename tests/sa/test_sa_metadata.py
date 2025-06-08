# -*- coding: utf-8 -*-

from mcp_ohmy_sql.sa.metadata import get_schema_info
from mcp_ohmy_sql.tests.chinook import metadata

from rich import print as rprint


def test_get_schema_info():
    schema_info = get_schema_info(metadata)
    # rprint(schema_info.model_dump())  # for debug only


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.sa.metadata",
        preview=False,
    )
