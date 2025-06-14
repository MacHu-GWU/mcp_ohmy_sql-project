# -*- coding: utf-8 -*-

import sqlalchemy as sa

from ..constants import DbTypeEnum


def get_create_view_sql(
    engine: sa.Engine,
    select: sa.Select,
    view_name: str,
    db_type: DbTypeEnum,
) -> str:
    """
    Generate SQL statement to create a view from a given select statement.

    :param engine: SQLAlchemy engine to compile the select statement.
    :param select: SQLAlchemy Select object representing the query for the view.
    :param view_name: Name of the view to be created.

    :return: SQL statement to create the view.
    """
    select_sql = select.compile(
        engine,
        compile_kwargs={"literal_binds": True},
    )
    if db_type is DbTypeEnum.SQLITE:
        create_view_sql = f'CREATE VIEW IF NOT EXISTS "{view_name}" AS {select_sql}'
    elif db_type is DbTypeEnum.POSTGRESQL:
        create_view_sql = f'CREATE OR REPLACE VIEW "{view_name}" AS {select_sql}'
    elif db_type is DbTypeEnum.MYSQL:  # pragma: no cover
        create_view_sql = f'CREATE OR REPLACE VIEW "{view_name}" AS {select_sql}'
    elif db_type is DbTypeEnum.MSSQL:  # pragma: no cover
        create_view_sql = f'CREATE OR ALTER VIEW "{view_name}" AS {select_sql}'
    elif db_type is DbTypeEnum.ORACLE:  # pragma: no cover
        create_view_sql = f'CREATE OR REPLACE VIEW "{view_name}" AS {select_sql}'
    else:  # pragma: no cover
        raise NotImplementedError(f"Unsupported database type: {db_type}")
    return create_view_sql


def get_drop_view_sql(
    view_name: str,
    db_type: DbTypeEnum,
) -> str:
    """
    Generate SQL statement to drop a view.

    :param view_name: Name of the view to be dropped.
    :param db_type: Type of the database (e.g., SQLite, PostgreSQL).

    :return: SQL statement to drop the view.
    """
    if db_type is DbTypeEnum.SQLITE:
        return f'DROP VIEW IF EXISTS "{view_name}"'
    elif db_type is DbTypeEnum.POSTGRESQL:
        return f'DROP VIEW IF EXISTS "{view_name}"'
    elif db_type is DbTypeEnum.MYSQL:  # pragma: no cover
        return f'DROP VIEW IF EXISTS "{view_name}"'
    elif db_type is DbTypeEnum.MSSQL:  # pragma: no cover
        raise NotImplementedError(f"Unsupported database type: {db_type}")
    elif db_type is DbTypeEnum.ORACLE:  # pragma: no cover
        raise NotImplementedError(f"Unsupported database type: {db_type}")
    else:  # pragma: no cover
        raise NotImplementedError(f"Unsupported database type: {db_type}")
