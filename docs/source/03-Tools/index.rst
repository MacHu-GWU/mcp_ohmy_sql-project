.. _tools-guide:

Tools Guide
==============================================================================
This guide provides a complete reference of all MCP tools available for database operations. These tools enable AI assistants to discover, analyze, and query your databases through natural language interactions.

- :meth:`list_databases <mcp_ohmy_sql.hub.tool_hub.ToolHubMixin.tool_list_databases>`: List all configured databases with their identifiers and descriptions
- :meth:`list_tables <mcp_ohmy_sql.hub.tool_hub.ToolHubMixin.tool_list_tables>`: Show all tables, views, and materialized views in a specific database schema
- :meth:`get_database_details <mcp_ohmy_sql.hub.tool_hub.ToolHubMixin.tool_get_database_details>`: Retrieve comprehensive schema information for all configured databases and schemas
- :meth:`get_schema_details <mcp_ohmy_sql.hub.tool_hub.ToolHubMixin.tool_get_schema_details>`: Get detailed schema information essential for writing accurate SQL queries (critical for SQL generation)
- :meth:`execute_select_statement <mcp_ohmy_sql.hub.tool_hub.ToolHubMixin.tool_execute_select_statement>`: Execute SELECT queries with performance monitoring and formatted results
