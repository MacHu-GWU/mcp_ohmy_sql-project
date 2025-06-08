# -*- coding: utf-8 -*-

from mcp_ohmy_sql.utils import match


def test_match():
    cases = [
        (
            "EMPLOYEES",
            ["employees"],
            [],
            True,
        ),
        (
            "EMPLOYEES",
            ["managers"],
            [],
            False,
        ),
    ]
    for name, include, exclude, expected in cases:
        assert match(name, include, exclude) == expected


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "final_sql_mcp.utils",
        preview=False,
    )
