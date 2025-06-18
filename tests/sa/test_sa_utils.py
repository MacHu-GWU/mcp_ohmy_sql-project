# -*- coding: utf-8 -*-

from mcp_ohmy_sql.constants import DbTypeEnum
from mcp_ohmy_sql.sa.utils import (
    get_create_view_sql,
    get_drop_view_sql,
    check_connection,
)
from mcp_ohmy_sql.tests.chinook.chinook_data_model import (
    ChinookViewNameEnum,
    album_sales_stats_view_select_stmt,
)


def setup_module(module):
    print("")


class TestSqlalchemyUtils:
    def test_get_create_view_sql(self, sqlite_sa_engine_objs):
        engine = sqlite_sa_engine_objs.engine
        sql = get_create_view_sql(
            engine=engine,
            select=album_sales_stats_view_select_stmt,
            view_name=ChinookViewNameEnum.AlbumSalesStats.name,
            db_type=DbTypeEnum.SQLITE,
        )
        # print(sql)  # for debug only

    def test_get_drop_view_sql(self):
        sql = get_drop_view_sql(
            view_name=ChinookViewNameEnum.AlbumSalesStats.name,
            db_type=DbTypeEnum.SQLITE,
        )
        # print(sql)  # for debug only

    def test_check_connection(self, sqlite_sa_engine_objs):
        engine = sqlite_sa_engine_objs.engine
        row = check_connection(engine)
        assert row == {"value": 1}


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.sa.utils",
        preview=False,
    )
