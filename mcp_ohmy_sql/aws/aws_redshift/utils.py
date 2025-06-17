# -*- coding: utf-8 -*-

import typing as T
from contextlib import contextmanager

import redshift_connector


@contextmanager
def Session(
    conn: redshift_connector.Connection,
) -> T.Generator[redshift_connector.Cursor, None, None]:
    cursor = conn.cursor()
    try:
        yield cursor
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
