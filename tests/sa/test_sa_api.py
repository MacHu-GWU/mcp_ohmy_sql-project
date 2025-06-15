# -*- coding: utf-8 -*-

from mcp_ohmy_sql.sa import api


def test():
    _ = api
    _ = api.get_create_view_sql
    _ = api.get_drop_view_sql
    _ = api.execute_count_query
    _ = api.execute_select_query


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.sa.api",
        preview=False,
    )
