# -*- coding: utf-8 -*-

import typing as T
from contextlib import contextmanager

from ...lazy_import import redshift_connector, sa


@contextmanager
def Session(
    conn: "redshift_connector.Connection",
) -> T.Generator["redshift_connector.Cursor", None, None]:
    cursor = conn.cursor()
    try:
        yield cursor
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


def execute_many_sql(
    conn_or_engine: T.Union[
        "redshift_connector.Connection",
        "sa.Engine",
    ],
    sql: T.Union[str, list[str]],
):
    """
    Utility function to execute multiple SQL statements.

    :param conn_or_engine: Redshift connection or SQLAlchemy engine.
    :param sql: A single SQL statement or a list of SQL statements to execute.
    """
    if isinstance(sql, str):
        sql_list = [sql]
    elif isinstance(sql, list):
        sql_list = sql
    else: # pragma: no cover
        raise TypeError("sql must be a str or a list of str")

    if isinstance(conn_or_engine, redshift_connector.Connection):
        with Session(conn_or_engine) as cursor:
            for sql in sql_list:
                cursor.execute(sql)
            conn_or_engine.commit()
    elif isinstance(conn_or_engine, sa.Engine):
        with conn_or_engine.connect() as conn:
            for sql in sql_list:
                conn.execute(sa.text(sql))
            conn.commit()
    else:  # pragma: no cover
        raise TypeError("conn_or_engine must be a redshift_connector.Connection")
