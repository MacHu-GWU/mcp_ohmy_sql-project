# -*- coding: utf-8 -*-

import typing as T
import time

from .server import mcp

from .config.config_init import config

from .sa.query import execute_count_query, execute_select_query


@mcp.tool()
async def get_database_schema() -> str:
    """
    Retrieve comprehensive database schema information for AI query assistance.

    This MCP tool performs database metadata inspection to extract complete structural
    information about all databases, all schemas, filtered tables, columns, relationships,
    and constraints in the connected database. The returned data provides LLMs
    with sufficient context to understand the database schema and write accurate SQL queries.

    The tool analyzes the database metadata and returns a structured JSON containing:

    - All table names and their full qualified names
    - Complete column definitions with data types, nullability, and properties
    - Primary key specifications for each table
    - Foreign key relationships with referential actions (CASCADE, SET NULL, etc.)
    - Column constraints (UNIQUE, CHECK, etc.)
    - Index information and computed column details
    - Autoincrement and identity column specifications

    This comprehensive schema information enables LLMs to:

    - Understand table relationships and design proper JOIN queries
    - Respect data types and constraints when generating SQL
    - Identify primary and foreign keys for correct record relationships
    - Write syntactically correct queries that align with the database structure

    :returns: A structured text that includes all databases, schema, filtered tables,
        columns, relationships, and constraints in the following formats
        optimized for LLM consumption.

    Database Schema Format::

        Database <Database 1 Identifier>(
          Schema <Schema 1 Name>(
            Table or View or MaterializedView <Table 1 Name>(
              ${COLUMN_NAME}:${DATA_TYPE}${PRIMARY_KEY}${UNIQUE}${NOT_NULL}${INDEX}${FOREIGN_KEY},
              more columns ...
            )
            more tables ...
          )
          more schemas ...
        )
        more databases ...

    There might be multiple Foreign Keys encoded as ``*FK->Table1.Column1*FK->Table2.Column2``.

    Constraints are encoded as:

    - *PK: Primary Key (implies unique and indexed)
    - *UQ: Unique constraint (implies indexed)
    - *NN: Not Null constraint
    - *IDX: Has database index
    - *FK->Table.Column: Foreign key reference

    Example output::

        Database chinook(
          Schema default(
            Table Album(
              AlbumId:INT*PK*NN,
              Title:STR*NN,
              ArtistId:INT*NN*FK->Artist.ArtistId,
            )
            Table Artist(
              ArtistId:INT*PK*NN,
              Name:STR,
            )
          )
        )

    Note:

        This tool requires no parameters and operates on the currently configured
        database connection. The metadata is cached for performance and reflects
        the database state at server startup.
    """
    return config.get_database_schema()


@mcp.tool()
async def execute_select_statement(
    database_identifier: str,
    sql: str,
    params: T.Optional[dict[str, T.Any]] = None,
) -> str:
    """
    Execute SQL SELECT statements with performance monitoring and result formatting.

    This MCP tool executes SELECT queries against the connected database and returns
    both execution timing information and formatted results. The execution time is
    critical for query optimization - use this data to identify slow queries that
    may need optimization through indexing, query restructuring, or result limiting.

    **Performance Monitoring:**

    - Execution time is measured in seconds with millisecond precision
    - Times > 1 second indicate potential optimization opportunities
    - Times > 5 seconds suggest immediate attention needed for query optimization
    - Consider adding WHERE clauses, LIMIT statements, or indexes for slow queries

    **Result Safety:**

    - Results are automatically limited to prevent overwhelming LLM context
    - Large datasets are truncated with indicators showing partial results
    - Use COUNT queries first to estimate result size before full SELECT

    :param sql: The SELECT statement to execute. Must be a valid SELECT query only.
        DDL, DML, and other non-SELECT statements are not permitted.
    :param params: Optional dictionary of parameter values for parameterized queries.
        Use this for safe value substitution (e.g., {"user_id": 123}).

    :returns: Formatted response containing:
        - Execution time in seconds (use this to assess query performance)
        - Query results formatted as a readable Markdown table
        - Arbitrary additional information

    Example usage::

        # Simple query
        execute_select_statement("SELECT * FROM users LIMIT 10")

        # Parameterized query (recommended for dynamic values)
        execute_select_statement(
            "SELECT * FROM orders WHERE user_id = :user_id LIMIT 20",
            {"user_id": 123}
        )

    Example output::

        # Execution Time
        0.045 seconds

        # Query Result
        | id | name     | email              |
        |----|----------|--------------------|
        | 1  | John Doe | john@example.com   |
        | 2  | Alice    | alice@example.com  |

    .. note::

        This tool is read-only and only accepts SELECT statements. Use the execution
        time feedback to guide query optimization decisions and ensure efficient
        database interactions that respect LLM context limitations.
    """
    start_time = time.time()
    if database_identifier not in config.databases_mapping:
        return f"Error: Database '{database_identifier}' not found in configuration."
    engine = config.databases_mapping[database_identifier].sa_engine
    query_result_text = execute_select_query(
        engine=engine,
        query=sql,
        params=params,
    )
    duration = time.time() - start_time
    lines = [
        "# Execution Time",
        f"{duration:.3f} seconds",
        "",
        "# Query Result",
        query_result_text,
    ]
    return "\n".join(lines)
