# -*- coding: utf-8 -*-

import typing as T
import time
import textwrap

from ..constants import TAB

from ..sa.api import (
    encode_schema_info,
    execute_select_query,
)

if T.TYPE_CHECKING:  # pragma: no cover
    from .hub import Hub


class ToolHubMixin:
    def tool_list_databases(self: "Hub") -> str:
        """
        List all configured databases available for querying.

        This MCP tool provides discovery of all databases configured in the server,
        showing their identifiers, schema counts, and descriptions. Use this tool
        when you need to understand what databases are available before performing
        any database operations.

        **When to use this tool:**
        - User asks "what databases do I have?"
        - Before selecting a database for schema exploration
        - When you need to show available data sources
        - To understand the scope of configured databases

        **Key Information Returned:**
        - Database identifier (used in other tools)
        - Number of schemas per database
        - Human-readable descriptions
        - Configuration summary

        :returns: A formatted string listing all configured databases with their
            identifiers, schema counts, and descriptions.

        Example output::

            Available Databases:

            - 'production_db': 3 schemas, Production PostgreSQL database
            - 'analytics_warehouse': 1 schemas, Data warehouse for reporting
            - 'chinook_sqlite': 1 schemas, Sample music store database
        """
        lines = [
            "Available Databases:",
        ]
        for database in self.config.databases:
            line = f"- {database.identifier!r}: {len(database.schemas)} schemas, {database.description or 'No description'})"
            lines.append(line)
        return "\n".join(lines)

    def tool_list_tables(
        self: "Hub",
        database_identifier: str,
        schema_name: T.Optional[str] = None,
    ) -> str:
        """
        List all tables, views, and materialized views in a specific database schema.

        This MCP tool provides a high-level overview of all database objects
        (tables, views, materialized views) in a specific schema, including their
        types and comments. Use this tool for quick discovery of available data
        sources before exploring detailed schema information.

        **When to use this tool:**
        - User asks "what tables are in this database?"
        - Quick overview of available data objects
        - Before diving into detailed schema exploration
        - To understand the scope of tables in a schema

        **Key Information Returned:**
        - Object type (Table, View, MaterializedView)
        - Object names (table/view names)
        - Comments or descriptions for each object
        - Filtered results based on configuration

        :param database_identifier: The identifier of the database to query
            (get this from list_databases tool).
        :param schema_name: Optional schema name to filter the results. If not
            provided or None, uses the default schema for the database.

        :returns: A formatted string listing all accessible tables, views, and
            materialized views with their types and comments.

        Example output::

            Available Tables, Views, and Materialized Views:

            - Table 'Album': Music album information
            - Table 'Artist': Recording artist details
            - Table 'Customer': Customer contact information
            - View 'AlbumSalesStats': Pre-calculated album sales metrics
            - Table 'Invoice': Sales transaction records
        """
        (flag, msg, database, schema) = self.get_database_and_schema_object(
            database_identifier, schema_name
        )
        if flag is False:
            return msg
        schema_info = self.get_schema_info(database, schema)
        lines = [
            "Available Tables, Views, and Materialized Views:",
        ]
        for table_info in schema_info.tables:
            line = f"- {table_info.object_type} {table_info.name!r}: {len(table_info.columns)} columns, {table_info.comment or 'No comment'}"
            lines.append(line)
        return "\n".join(lines)

    def tool_get_database_details(self: "Hub") -> str:
        """
        Retrieve comprehensive database, schema, table, information for AI query assistance.

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

        Database Schema Format:

        .. code-block:: typescript

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

        - ``*PK``: Primary Key (implies unique and indexed)
        - ``*UQ``: Unique constraint (implies indexed)
        - ``*NN``: Not Null constraint
        - ``*IDX``: Has database index
        - ``*FK->Table.Column``: Foreign key reference

        Example output:

        .. code-block:: typescript

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
        database_lines = []
        for database in self.config.databases:
            schema_lines = []
            for schema in database.schemas:
                schema_info = self.get_schema_info(database, schema)
                s = encode_schema_info(schema_info)
                schema_lines.append(textwrap.indent(s, prefix=TAB))
            schemas_def = "\n".join(schema_lines)
            s = f"Database {database.identifier}(\n{schemas_def}\n)"
            database_lines.append(s)
        databases_def = "\n".join(database_lines)
        return databases_def

    def tool_get_schema_details(
        self: "Hub",
        database_identifier: str,
        schema_name: T.Optional[str] = None,
    ) -> str:
        """
        Get detailed schema information essential for writing accurate SQL queries.

        **CRITICAL FOR SQL QUERY WRITING**: This is the most important tool for SQL
        generation. ALWAYS use this tool before writing any SQL query to get the
        exact table structure, column names, data types, and relationships.

        **MANDATORY USAGE BEFORE SQL QUERIES:**

        - Get exact column names and data types
        - Understand table relationships and foreign keys
        - Identify primary keys for JOIN operations
        - Verify table and view names exist
        - Check constraints and nullable columns
        - Understand database-specific data types

        **Schema Encoding Format:**

        The output uses a special compact format optimized for LLM consumption:

        - Tables: ``Table TableName(columns...)``
        - Views: ``View ViewName(columns...)``
        - Columns: ``ColumnName:DataType*Constraints``
        - Constraints: ``*PK`` (Primary Key), ``*FK->Table.Column`` (Foreign Key),
          ``*NN`` (Not Null), ``*UQ`` (Unique), ``*IDX`` (Indexed)

        **What this tool provides:**

        - Complete table and view structures
        - All column names with exact spelling/case
        - Data types mapped to simple categories (INT, STR, DEC, DT, TS, etc.)
        - Primary and foreign key relationships
        - Constraint information for safe query writing
        - Filtered tables based on configuration

        :param database_identifier: The identifier of the database to analyze
            (obtained from list_databases tool).
        :param schema_name: Optional schema name. If not provided or None,
            uses the default schema for the database.

        :returns: Compact schema representation showing all tables, columns,
            data types, and relationships in the specified schema.

        Example output:

        .. code-block:: typescript

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
              View AlbumSalesStats(
                AlbumId:INT,
                AlbumTitle:STR,
                TotalRevenue:DEC,
              )
            )

        .. important::

            **AI Assistants MUST use this tool before writing SQL queries** to ensure:

            1. Correct table and column names (exact spelling/case)
            2. Proper JOIN syntax using foreign key relationships
            3. Appropriate data type handling in WHERE clauses
            4. Awareness of NOT NULL constraints
            5. Understanding of available tables and views
        """
        (flag, msg, database, schema) = self.get_database_and_schema_object(
            database_identifier, schema_name
        )
        if flag is False:
            return msg
        schema_info = self.get_schema_info(database, schema)
        s = encode_schema_info(schema_info)
        return s

    def tool_execute_select_statement(
        self: "Hub",
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

        :param database_identifier: The identifier of the database to query
            (obtained from list_databases tool).
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
        if database_identifier not in self.config.databases_mapping:
            return (
                f"Error: Database '{database_identifier}' not found in configuration."
            )
        engine = self.config.databases_mapping[database_identifier].sa_engine
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
