# -*- coding: utf-8 -*-

import typing as T
import time

from .server import mcp
from .config_init import config

from .sa.metadata import get_schema_info, SchemaInfo
from .sa.query import execute_count_query, execute_select_query


@mcp.tool()
async def get_database_schema_info() -> SchemaInfo:
    """
    Retrieve comprehensive database schema information for AI query assistance.

    This MCP tool performs database metadata inspection to extract complete structural
    information about all tables, columns, relationships, and constraints in the
    connected database. The returned data provides LLMs with sufficient context to
    understand the database schema and write accurate SQL queries.

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

    :returns: :class:`~final_sql_mcp.sa.metadata.SchemaInfo`
        A structured Pydantic model containing complete database schema
        information organized hierarchically (schema -> tables -> columns)
        with all metadata necessary for intelligent query generation.

    Example output::

        {
            "object_type": "schema",
            "name": "public",
            "tables": [
                {
                    "object_type": "table",
                    "name": "users",
                    "fullname": "public.users",
                    "primary_key": [
                        "id"
                    ],
                    "foreign_keys": [],
                    "columns": [
                        {
                            "object_type": "column",
                            "name": "id",
                            "fullname": "users.id",
                            "type": "INTEGER",
                            "nullable": false,
                            "index": true,
                            "unique": true,
                            "system": false,
                            "doc": "",
                            "comment": "Primary key",
                            "autoincrement": "auto",
                            "constraints": [
                                "PRIMARY KEY"
                            ],
                            "foreign_keys": [],
                            "computed": false,
                            "identity": false
                        },
                        {
                            "object_type": "column",
                            "name": "email",
                            "fullname": "users.email",
                            "type": "VARCHAR(255)",
                            "nullable": false,
                            "index": true,
                            "unique": true,
                            "system": false,
                            "doc": "",
                            "comment": "",
                            "autoincrement": "false",
                            "constraints": [
                                "UNIQUE",
                                "NOT NULL"
                            ],
                            "foreign_keys": [],
                            "computed": false,
                            "identity": false
                        }
                    ]
                },
                {
                    "object_type": "table",
                    "name": "orders",
                    "fullname": "public.orders",
                    "primary_key": [
                        "id"
                    ],
                    "foreign_keys": [
                        {
                            "object_type": "foreign key",
                            "name": "user_id",
                            "comment": "References users table",
                            "onupdate": "CASCADE",
                            "ondelete": "SET NULL",
                            "deferrable": false,
                            "initially": "IMMEDIATE"
                        }
                    ],
                    "columns": [
                        {
                            "object_type": "column",
                            "name": "user_id",
                            "fullname": "orders.user_id",
                            "type": "INTEGER",
                            "nullable": true,
                            "index": true,
                            "unique": false,
                            "system": false,
                            "doc": "",
                            "comment": "",
                            "autoincrement": "false",
                            "constraints": [
                                "FOREIGN KEY"
                            ],
                            "foreign_keys": [
                                {
                                    "object_type": "foreign key",
                                    "name": "user_id",
                                    "comment": "References users table",
                                    "onupdate": "CASCADE",
                                    "ondelete": "SET NULL",
                                    "deferrable": false,
                                    "initially": "IMMEDIATE"
                                }
                            ],
                            "computed": false,
                            "identity": false
                        }
                    ]
                }
            ]
        }

    Note:

        This tool requires no parameters and operates on the currently configured
        database connection. The metadata is cached for performance and reflects
        the database state at server startup.
    """
    return get_schema_info(metadata=config.metadata)


@mcp.tool()
async def execute_select_statement(
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
    query_result_text = execute_select_query(
        engine=config.engine,
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
