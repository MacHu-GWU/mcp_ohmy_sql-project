# -*- coding: utf-8 -*-

from mcp_ohmy_sql.sa.query import (
    ensure_valid_select_query,
    execute_count_query,
    execute_select_query,
)

import pytest


def setup_module(module):
    print("")


class TestSqlalchemyQuery:
    def test_ensure_valid_select_query(self, sqlite_sa_engine_objs):
        with pytest.raises(ValueError):
            ensure_valid_select_query("INVALID SQL QUERY HERE")

    def test_execute_count_query(self, sqlite_sa_engine_objs):
        engine = sqlite_sa_engine_objs.engine

        count = execute_count_query(
            engine=engine,
            query="SELECT * FROM Album LIMIT 3",
        )
        assert count == 3

        count = execute_count_query(
            engine=engine,
            query="SELECT * FROM Album LIMIT 3;",
        )
        assert count == 3

    def test_execute_select_query(self, sqlite_sa_engine_objs):
        engine = sqlite_sa_engine_objs.engine

        result = execute_select_query(
            engine=engine,
            query="SELECT * FROM Album LIMIT 3",
        )
        # print(result)  # for debug only

        result = execute_select_query(
            engine=engine,
            query="SELECT * FROM Album LIMIT 3;",
        )
        # print(result)  # for debug only

        result = execute_select_query(
            engine=engine,
            query="SELECT INVALID SQL QUERY HERE",
        )
        # print(result)
        assert "OperationalError" in result

        result = execute_select_query(
            engine=engine,
            query="SELECT * FROM Album WHERE AlbumId >= 999999",
        )
        # print(result)  # for debug only
        assert "No result" in result


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.sa.query",
        preview=False,
    )
