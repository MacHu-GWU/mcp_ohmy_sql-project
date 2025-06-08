# -*- coding: utf-8 -*-

import typing as T
import sqlalchemy as sa
from tabulate import tabulate
from pydantic import BaseModel, Field

try:  # pragma: no cover
    from rich import print as rprint
except ImportError:  # pragma: no cover
    pass


def format_result(
    result: T.Union[sa.CursorResult, sa.Result],
) -> str:
    """
    Format SQL query result into a Markdown table.

    .. note::

        Markdown tables are the optimal format for presenting SQL query results to LLMs,
        offering the best combination of token efficiency, comprehension, and maintainability.

        - Token Efficiency: Uses 24% fewer tokens than JSON, reducing API costs
            and fitting more data within context limits
        - Natural LLM Comprehension: Aligns with LLM training data patterns,
            enabling better understanding compared to nested JSON/XML structures
        - Balanced Readability: Maintains both machine parsability and human readability
            for seamless debugging and maintenance
    """
    rows = list()
    try:
        first_item: sa.Row = next(result)
        keys, values = list(first_item._fields), list(first_item)
        rows.append(keys)
        rows.append(values)
    except StopIteration:
        return "No result"
    for row in result:
        rows.append(list(row))

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
        return "Invalid query: must start with 'SELECT '"


def execute_count_query(
    engine: sa.Engine,
    query: str,
    params: T.Optional[dict[str, T.Any]] = None,
) -> int:
    """
    Executes a SQL SELECT query and returns the count of rows.
    """
    ensure_valid_select_query(query)

    # use engine.dialect.name is the most reliable way to detect database type
    if engine.dialect.name == "sqlite":
        count_query = f"SELECT COUNT(*) FROM ({query}) AS subquery"
        count_stmt = sa.text(count_query)
    else:
        raw_stmt = sa.text(query)
        subq = raw_stmt.subquery("anon_subq")  # anonymous subquery
        count_stmt = sa.select(sa.func.count()).select_from(subq)

    with engine.connect() as connection:
        result = connection.execute(count_stmt, params)
        count = result.fetchone()[0]
        return count


def execute_select_query(
    engine: sa.Engine,
    query: str,
    params: T.Optional[dict[str, T.Any]] = None,
) -> str:
    """
    Executes a SQL SELECT query and returns the result formatted as a Markdown table.
    """
    ensure_valid_select_query(query)

    stmt = sa.text(query)
    with engine.connect() as connection:
        try:
            result = connection.execute(stmt, params)
        except Exception as e:
            return f"Error executing query: {e}"

        try:
            text = format_result(result)
        except Exception as e:
            return f"Error formatting result: {e}"

        return text
