.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

1. Add local query result caching for offline data analysis and export capabilities.
2. Add persistent query history with named cache for session resumption and reference.
3. Add ElasticSearch/OpenSearch database support with SQL interface integration.
4. Add comprehensive database/schema/table management tools with enhanced metadata access.
5. Add external knowledge base integration for business context and data dictionary enrichment.
6. Add MongoDB database support with Atlas SQL interface compatibility.
7. Add AWS Glue Catalog integration for data lake and warehouse metadata discovery.

**Minor Improvements**

- Add configurable TTL cache for database schema metadata to improve performance.

**Bugfixes**

**Miscellaneous**


0.1.3 (2025-06-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- **AWS Redshift Support**: Complete integration with Redshift Serverless and provisioned clusters via boto3.

**Minor Improvements**

- Enhanced error messaging: Provide actionable troubleshooting guidance for database connection failures.
- Enhanced error messaging: Include specific schema details when metadata extraction fails.
- Enhanced error messaging: Return detailed SQL execution context and suggestions for query failures.

**Miscellaneous**

- **Major Architecture Refactor**: Implemented modular adapter-based design with clear separation between configuration, database operations, and MCP tools.
- **Improved Testing Infrastructure**: Migrated to pytest fixture-based database provisioning with real SQLite, PostgreSQL, and AWS Redshift instances.


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
