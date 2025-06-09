# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.sa",
        is_folder=True,
        preview=False,
    )
