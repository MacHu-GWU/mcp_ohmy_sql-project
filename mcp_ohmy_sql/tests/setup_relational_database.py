# -*- coding: utf-8 -*-

"""
Test Relational Database Setup Module

This module provides automated setup functionality for creating and populating test databases
with the Chinook sample dataset. It supports multiple database backends including SQLite and
PostgreSQL, making it easy to provision identical test environments across different database
systems.

Key Features:

- Automated schema creation using SQLAlchemy ORM models
- Data population from Chinook JSON dataset
- Cross-database compatibility (SQLite, PostgreSQL)
- Sample view creation for testing complex queries
- Idempotent operations (safe to run multiple times)
"""


import sqlalchemy as sa
from ..constants import DbTypeEnum
from ..sa.api import get_create_view_sql, get_drop_view_sql

from .chinook.chinook_data_model import (
    ChinookViewNameEnum,
    VIEW_NAME_AND_SELECT_STMT_MAP,
)
from .chinook.chinook_data_loader import chinook_data_loader


def drop_all_tables(
    engine: sa.Engine,
    metadata: sa.MetaData,
):
    """
    Drop all tables in the given SQLAlchemy metadata.
    """
    metadata.drop_all(engine, checkfirst=True)


def create_all_tables(
    engine: sa.Engine,
    metadata: sa.MetaData,
    drop_first: bool = True,
):
    """
    Create all tables in the given SQLAlchemy metadata.
    """
    if drop_first:
        drop_all_tables(engine=engine, metadata=metadata)
    metadata.create_all(engine, checkfirst=True)


def drop_all_views(
    engine: sa.Engine,
    db_type: DbTypeEnum,
):
    """
    Drop all views defined in the ChinookViewNameEnum.
    """
    view_name_list = [view_name.value for view_name in ChinookViewNameEnum]
    view_name_list = view_name_list[::-1]  # reverse order to drop views first
    with engine.connect() as conn:
        for view_name in view_name_list:
            drop_view_sql = get_drop_view_sql(
                view_name=view_name,
                db_type=db_type,
            )
            stmt = sa.text(drop_view_sql)
            conn.execute(stmt)
        conn.commit()


def create_all_views(
    engine: sa.Engine,
    db_type: DbTypeEnum,
):
    """
    Create all views defined in the ChinookViewNameEnum.
    """
    with engine.connect() as conn:
        for view_name_enum in ChinookViewNameEnum:
            view_name = view_name_enum.value
            select_stmt = VIEW_NAME_AND_SELECT_STMT_MAP[view_name]
            create_view_sql = get_create_view_sql(
                engine=engine,
                view_name=view_name,
                select=select_stmt,
                db_type=db_type,
            )
            conn.execute(sa.text(create_view_sql))
        conn.commit()


def insert_all_data(
    engine: sa.Engine,
    metadata: sa.MetaData,
):
    """
    Insert all data into the database tables defined in the metadata.
    """
    with engine.connect() as conn:
        for table in metadata.sorted_tables:
            stmt = sa.insert(table)
            df = chinook_data_loader.get_table_df(table.name)
            rows = df.to_dicts()
            conn.execute(stmt, rows)
        conn.commit()
