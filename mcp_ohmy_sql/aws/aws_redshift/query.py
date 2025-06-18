# -*- coding: utf-8 -*-

import typing as T

from tabulate import tabulate

from ...lazy_import import redshift_connector

from .utils import Session


try:  # pragma: no cover
    from rich import print as rprint
except ImportError:  # pragma: no cover
    pass


def format_result(
    columns: list[str],
    records: list[tuple],
) -> str:
    """
    Format SQL query result into a Markdown table.
    """
    rows = list()
    rows.append(columns)
    rows.extend(records)
    text = tabulate(
        rows,
        headers="firstrow",
        tablefmt="pipe",
        floatfmt=".4f",
    )
    return text


def ensure_valid_select_query(query: str):
    """
    Ensure the query is a valid SELECT statement.
    """
    if query.upper().strip().startswith("SELECT ") is False:
        raise ValueError("Invalid query: must start with 'SELECT '")


def execute_select_query(
    conn: "redshift_connector.Connection",
    query: str,
    params: T.Optional[dict[str, T.Any]] = None,
) -> str:
    """
    Executes a SQL SELECT query and returns the result formatted as a Markdown table.
    """
    try:
        ensure_valid_select_query(query)
    except ValueError as e:  # pragma: no cover
        return f"Error: {e}"

    with Session(conn) as cursor:
        try:
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
        except Exception as e:  # pragma: no cover
            return f"Error executing query: {e}"

    try:
        text = format_result(columns, rows)
    except Exception as e:  # pragma: no cover
        return f"Error formatting result: {e}"

    return text
