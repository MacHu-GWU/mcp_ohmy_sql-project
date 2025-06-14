# -*- coding: utf-8 -*-

import typing as T

import pytest
import sqlalchemy as sa

from mcp_ohmy_sql.constants import DbTypeEnum
from mcp_ohmy_sql.sa.utils import get_create_view_sql
from mcp_ohmy_sql.tests.chinook.chinook_data_model import (
    Base,
    VIEW_NAME_AND_SELECT_STMT_MAP,
    ChinookViewNameEnum,
    album_sales_stats_view_select_stmt,
)


@pytest.fixture(scope="function")
def in_memory_sqlite_engine() -> T.Generator[sa.Engine, None, None]:
    """
    Fixture to create an in-memory SQLite database engine for testing.

    This fixture sets up a new SQLite database in memory, creates the necessary tables,
    and returns the engine. The database is reset after each test function.
    """
    engine = sa.create_engine("sqlite:///:memory:")

    # create tables
    Base.metadata.create_all(engine)

    # create views
    with engine.connect() as conn:
        for view_name, select_stmt in VIEW_NAME_AND_SELECT_STMT_MAP.items():
            create_view_sql = get_create_view_sql(
                engine=engine,
                view_name=view_name,
                select=select_stmt,
                db_type=DbTypeEnum.SQLITE,
            )
            conn.execute(sa.text(create_view_sql))
        conn.commit()

    # get the latest metadata with views
    metadata = sa.MetaData()
    metadata.reflect(engine, views=True)

    yield engine

    # drop views
    with engine.connect() as conn:
        view_name_list = list(VIEW_NAME_AND_SELECT_STMT_MAP)
        view_name_list = view_name_list[::-1]  # reverse order to drop views first
        for view_name in view_name_list:
            sql = f'DROP VIEW IF EXISTS "{view_name}"'
            stmt = sa.text(sql)
            conn.execute(stmt)
        conn.commit()

    # drop tables
    Base.metadata.drop_all(engine)  # this method doesn't drop views
