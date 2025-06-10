.. _tools-guide:

Tools Guide
==============================================================================
This guide provides a complete reference of all MCP tools available for database operations. These tools enable AI assistants to discover, analyze, and query your databases through natural language interactions.

- :func:`~mcp_ohmy_sql.tools.get_database_schema_details`: Retrieve comprehensive schema information for all configured databases and schemas
- :func:`~mcp_ohmy_sql.tools.list_databases`: List all configured databases with their identifiers and descriptions  
- :func:`~mcp_ohmy_sql.tools.list_tables`: Show all tables, views, and materialized views in a specific database schema
- :func:`~mcp_ohmy_sql.tools.get_schema_details`: Get detailed schema information essential for writing accurate SQL queries (critical for SQL generation)
- :func:`~mcp_ohmy_sql.tools.execute_select_statement`: Execute SELECT queries with performance monitoring and formatted results
