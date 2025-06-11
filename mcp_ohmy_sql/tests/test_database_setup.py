# -*- coding: utf-8 -*-

"""
Test Database Setup Module

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

Typical Usage:
    >>> from mcp_ohmy_sql.tests.test_database_setup import setup_test_database, EngineEnum
    >>> 
    >>> # Setup SQLite test database
    >>> setup_test_database(EngineEnum.sqlite)
    >>> 
    >>> # Setup PostgreSQL test database
    >>> setup_test_database(EngineEnum.postgres)
"""

from functools import cached_property

import sqlalchemy as sa

from .chinook.chinook_data_model import (
    ChinookViewNameEnum,
    Base,
    album_sales_stats_view_select_stmt,
)
from .chinook.chinook_data_loader import chinook_data_loader

from .test_config import DatabaseEnum


class _EngineEnum:
    @cached_property
    def sqlite(self) -> sa.engine.Engine:
        kwargs = DatabaseEnum.chinook_sqlite.connection.create_engine_kwargs
        return sa.create_engine(**kwargs)

    @cached_property
    def postgres(self) -> sa.engine.Engine:
        kwargs = DatabaseEnum.chinook_postgres.connection.create_engine_kwargs
        return sa.create_engine(**kwargs)


EngineEnum = _EngineEnum()


def drop_view(engine: sa.engine.Engine, view_name: str):
    with engine.connect() as conn:
        drop_view_sql = f'DROP VIEW IF EXISTS "{view_name}"'
        conn.execute(sa.text(drop_view_sql))
        conn.commit()


def drop_all_views(engine: sa.engine.Engine):
    for view_name in ChinookViewNameEnum:
        drop_view(engine, view_name.value)


def setup_test_database(engine: sa.engine.Engine) -> None:
    """
    Set up a complete test database with Chinook sample data and views.

    This function performs a comprehensive database setup by:

    1. Dropping all existing tables (if any) to ensure a clean state
    2. Creating all tables using SQLAlchemy ORM models based on the Chinook schema
    3. Loading sample data from the Chinook JSON dataset
    4. Converting datetime strings to proper datetime objects for database compatibility
    5. Creating sample views (like AlbumSalesStats) for testing complex queries

    The setup is idempotent - it can be run multiple times safely as it drops
    existing tables before recreation.

    Example:

        >>> from mcp_ohmy_sql.tests.test_database_setup import setup_test_database, EngineEnum
        >>>
        >>> # Setup SQLite test database
        >>> setup_test_database(EngineEnum.sqlite)
        >>>
        >>> # Setup PostgreSQL test database (requires running postgres container)
        >>> setup_test_database(EngineEnum.postgres)

    .. note::

        - For PostgreSQL, ensure the database server is running and accessible
        - The function automatically handles database-specific SQL differences
        - All foreign key relationships are properly maintained during data insertion
    """
    drop_all_views(engine)

    with engine.connect() as conn:
        Base.metadata.drop_all(engine, checkfirst=True)
        Base.metadata.create_all(engine, checkfirst=True)
        conn.commit()

    # Load data into tables
    with engine.connect() as conn:
        for table in Base.metadata.sorted_tables:

            stmt = sa.insert(table)
            df = chinook_data_loader.get_table_df(table.name)
            rows = df.to_dicts()
            conn.execute(stmt, rows)
        conn.commit()

    # Load data into views
    with engine.connect() as conn:
        select_sql = album_sales_stats_view_select_stmt.compile(
            engine,
            compile_kwargs={"literal_binds": True},
        )
        create_view_sql = f'CREATE VIEW "AlbumSalesStats" AS {select_sql}'
        # print(create_view_sql)
        conn.execute(sa.text(create_view_sql))
        conn.commit()
