.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.2 (2025-06-11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- **MCP Tools Available**:
    - ``list_databases()``: List all configured databases with identifiers and descriptions
    - ``list_tables()``: List tables, views, and materialized views in a database schema
    - ``get_database_details()``: Get complete schema information for all configured databases
    - ``get_schema_details()``: Get detailed schema for a specific database (essential for SQL writing)
    - ``execute_select_statement()``: Execute SELECT queries with performance timing and formatted results
- **Local MCP Server**: Support for local deployment using ``uv`` package manager
- **Multi-Database Support**: Connect to multiple databases simultaneously with individual configurations
- **Multi-Schema Support**: Access multiple schemas within each database
- **Table Filtering**: Include/exclude specific tables using pattern matching
- **Database Support**: SQLite, PostgreSQL, MySQL, SQL Server, Oracle via SQLAlchemy
- **Documentation Website**: Comprehensive documentation at https://mcp-ohmy-sql.readthedocs.io/
- **100% Code Coverage**: Achieved complete test coverage across all modules


0.1.1 (2025-06-07)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First release
- Register the package name on PyPI
