.. _configuration-guide:

Configuration Guide
==============================================================================
The ``mcp_ohmy_sql`` MCP server uses a flexible JSON-based configuration system that supports multiple databases and schemas. This guide is organized into focused sections to help you configure the server for your specific database setup.

.. autotoctree::
    :maxdepth: 1


Quick Start
------------------------------------------------------------------------------
1. **Set the configuration file path**:

   .. code-block:: bash

       export MCP_OHMY_SQL_CONFIG=/path/to/your/config.json

2. :ref:`Create a basic configuration file <basic-configuration>`
3. :ref:`Add your databases <database-configuration>`
4. :ref:`Configure schemas and table filters <schema-configuration>`
5. :ref:`Set up database connections <connection-configuration>`


Configuration Sections
------------------------------------------------------------------------------
:ref:`basic-configuration`:
    Learn the basic structure of the configuration file, including version, settings, and the overall JSON schema.

:ref:`database-configuration`:
    Understand how to define multiple databases, including identifiers, descriptions, and database-level settings.

:ref:`schema-configuration`
    Configure schemas within databases, including table filtering and schema-specific access controls.

:ref:`connection-configuration`
    Set up SQLAlchemy connections with proper connection strings and engine parameters.

:ref:`relational-database-connection-configuration`
    Detailed configuration examples for popular relational databases like PostgreSQL, MySQL, SQLite, and SQL Server.

:ref:`aws-redshift-connection-configuration`
    Specialized configuration for AWS Redshift data warehouses, including authentication and optimization settings.


What You'll Learn
------------------------------------------------------------------------------
- How to structure JSON configuration files
- Database connection setup for multiple database types
- Schema and table filtering strategies
- Security best practices for credentials
- Connection pooling and performance optimization
- Troubleshooting common configuration issues


Next Steps
------------------------------------------------------------------------------
After completing your configuration:

1. Start the MCP server with your configuration
2. Use the ``get_database_schema`` tool to verify your databases are accessible
3. Begin querying your databases through the AI assistant

For more information on available tools and their usage, see the :ref:`tools-guide` documentation.
