# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from final_sql_mcp.tests import run_cov_test

    run_cov_test(
        __file__,
        "final_sql_mcp.sa",
        is_folder=True,
        preview=False,
    )
