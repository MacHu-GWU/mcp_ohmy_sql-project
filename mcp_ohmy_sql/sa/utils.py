# -*- coding: utf-8 -*-

import sqlalchemy as sa


def get_create_view_sql(
    engine: sa.Engine,
    select: sa.Select,
    view_name: str,
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
    create_view_sql = f'CREATE VIEW "{view_name}" AS {select_sql}'
    return create_view_sql
