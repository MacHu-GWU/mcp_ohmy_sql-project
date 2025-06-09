Configuration Guide
==============================================================================
The ``mcp_ohmy_sql`` MCP server uses a flexible JSON-based configuration system that supports multiple databases and schemas. This guide explains how to configure the server for your specific database setup.


Configuration Loading Mechanism
------------------------------------------------------------------------------
The configuration system uses an environment variable to locate your configuration file:

.. code-block:: bash

    export MCP_OHMY_SQL_CONFIG=/path/to/your/config.json

When the MCP server starts, it reads this environment variable and loads the JSON configuration file from the specified path. If the environment variable is not set, the server will fail to start with an appropriate error message.


Configuration File Structure
------------------------------------------------------------------------------
The configuration file is a JSON document with the following top-level structure:

.. code-block:: json

    {
        "version": "0.1.1",
        "settings": {},
        "databases": []
    }


Root Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* ``version`` (string, required): The configuration schema version. Currently must be ``"0.1.1"``.
* ``settings`` (object, optional): Global settings for the MCP server. Currently empty but reserved for future use.
* ``databases`` (array, required): List of database configurations. Can be empty, but the field must exist.


Database Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Each database in the ``databases`` array has the following structure:

.. code-block:: json

    {
        "identifier": "unique_database_id",
        "description": "Human-readable description",
        "connection": {
            "type": "sqlalchemy",
            "create_engine_kwargs": {}
        },
        "schemas": []
    }

**Database Fields**

* ``identifier`` (string, required): A unique identifier for this database. Used in MCP tools to reference specific databases.
* ``description`` (string, optional): A human-readable description of the database purpose or contents.
* ``connection`` (object, required): Database connection configuration.
* ``schemas`` (array, required): List of schema configurations for this database.


Connection Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Currently, only SQLAlchemy connections are supported:

.. code-block:: json

    {
        "type": "sqlalchemy",
        "create_engine_kwargs": {
            "url": "dialect+driver://username:password@host:port/database"
        }
    }

* ``type`` (string, required): Must be ``"sqlalchemy"`` for SQLAlchemy connections.
* ``create_engine_kwargs`` (object, required): Parameters passed directly to SQLAlchemy's ``create_engine()`` function.

The ``create_engine_kwargs`` object supports all parameters accepted by SQLAlchemy's ``create_engine()`` function. The most common parameter is ``url``, which specifies the database connection string. For detailed information about connection URLs and other engine parameters, see the `SQLAlchemy Engine Configuration documentation <https://docs.sqlalchemy.org/en/20/core/engines.html>`_.

Common database URL formats:

* **SQLite**: ``sqlite:///path/to/database.db`` or ``sqlite:////absolute/path/to/database.db``
* **PostgreSQL**: ``postgresql+psycopg2://user:password@localhost:5432/dbname``
* **MySQL**: ``mysql+mysqldb://user:password@localhost:3306/dbname``


Schema Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Each schema in the ``schemas`` array has the following structure:

.. code-block:: json

    {
        "name": "schema_name", // optional, defaults to database's default schema
        "table_filter": {
            "include": ["table1", "table2"],
            "exclude": ["temp_*", "backup_*"]
        }
    }

**Schema Fields**

* ``name`` (string, optional): The schema name. If ``null`` or omitted, uses the database's default schema.
* ``table_filter`` (object, optional): Filters to include or exclude specific tables.

**Table Filter Configuration**

* ``include`` (array of strings, optional): Whitelist of table names to include. If empty, includes all tables not in exclude list.
* ``exclude`` (array of strings, optional): Blacklist of table names to exclude. Supports wildcards with ``*``.

.. note::

    When both ``include`` and ``exclude`` are specified, tables must be in the include list AND not in the exclude list to be accessible.


Complete Configuration Example
------------------------------------------------------------------------------
Here's a comprehensive example showing multiple databases with different configurations:

.. code-block:: json

    {
        "version": "0.1.1",
        "settings": {},
        "databases": [
            {
                "identifier": "local_dev",
                "description": "Local development SQLite database",
                "connection": {
                    "type": "sqlalchemy",
                    "create_engine_kwargs": {
                        "url": "sqlite:////home/user/dev/app.db"
                    }
                },
                "schemas": [
                    {
                        "name": null,
                        "table_filter": {
                            "include": [],
                            "exclude": ["_migrations", "temp_*"]
                        }
                    }
                ]
            },
            {
                "identifier": "analytics_prod",
                "description": "Production PostgreSQL analytics database",
                "connection": {
                    "type": "sqlalchemy",
                    "create_engine_kwargs": {
                        "url": "postgresql+psycopg2://analyst:password@analytics.company.com:5432/warehouse",
                        "pool_size": 5,
                        "max_overflow": 10,
                        "pool_pre_ping": true,
                        "echo": false
                    }
                },
                "schemas": [
                    {
                        "name": "public",
                        "table_filter": {
                            "include": [],
                            "exclude": []
                        }
                    },
                    {
                        "name": "reporting",
                        "table_filter": {
                            "include": ["sales_summary", "customer_metrics", "product_performance"],
                            "exclude": []
                        }
                    }
                ]
            },
            {
                "identifier": "mysql_inventory",
                "description": "MySQL inventory management system",
                "connection": {
                    "type": "sqlalchemy",
                    "create_engine_kwargs": {
                        "url": "mysql+mysqldb://inventory_user:secure_pass@10.0.1.50:3306/inventory",
                        "connect_args": {
                            "charset": "utf8mb4",
                            "connect_timeout": 10
                        }
                    }
                },
                "schemas": [
                    {
                        "name": "inventory",
                        "table_filter": {
                            "include": [],
                            "exclude": ["audit_*", "backup_*"]
                        }
                    }
                ]
            }
        ]
    }


Best Practices
------------------------------------------------------------------------------
1. **Use descriptive identifiers**: Choose database identifiers that clearly indicate the database purpose (e.g., ``sales_prod``, ``analytics_dev``).

2. **Secure your credentials**:
   * Never commit configuration files with passwords to version control
   * Consider using environment variables in your connection URLs:
     
     .. code-block:: json

         "url": "postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:5432/mydb"

   * Or use separate credential management systems

3. **Optimize connection pools**: For production databases, configure appropriate connection pool settings:

   .. code-block:: json

       "create_engine_kwargs": {
           "url": "postgresql://...",
           "pool_size": 10,
           "max_overflow": 20,
           "pool_timeout": 30,
           "pool_recycle": 3600
       }

4. **Filter unnecessary tables**: Use table filters to exclude system tables, temporary tables, or sensitive data:

   .. code-block:: json

       "table_filter": {
           "exclude": ["pg_*", "information_schema", "tmp_*", "user_passwords"]
       }

5. **Document your schemas**: Use the ``description`` field to document what each database contains and its purpose.


Troubleshooting
------------------------------------------------------------------------------


Common Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. **Configuration file not found**:
   
   * Ensure ``MCP_OHMY_SQL_CONFIG`` environment variable is set
   * Check the file path is absolute and accessible
   * Verify file permissions

2. **Database connection failures**:
   
   * Verify the connection URL is correct
   * Ensure database drivers are installed (e.g., ``psycopg2`` for PostgreSQL)
   * Check network connectivity and firewall rules
   * Test the connection string using SQLAlchemy directly

3. **Schema not found**:
   
   * Some databases are case-sensitive for schema names
   * Verify the schema exists in the database
   * Check user permissions for the schema


Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The configuration is validated when loaded. Common validation errors:

* Missing required fields (``version``, ``databases``)
* Invalid version number
* Duplicate database identifiers
* Invalid connection type (must be ``"sqlalchemy"``)


Environment-Specific Configurations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For different environments, maintain separate configuration files:

.. code-block:: bash

    # Development
    export MCP_OHMY_SQL_CONFIG=${HOME}/mcp_ohmy_sql.dev.json

    # Staging
    export MCP_OHMY_SQL_CONFIG=${HOME}/mcp_ohmy_sql.test.json

    # Production
    export MCP_OHMY_SQL_CONFIG=${HOME}/mcp_ohmy_sql.prod.json

This approach allows you to:

* Use different databases for different environments
* Apply stricter filters in production
* Adjust connection pool settings based on load
* Control access to sensitive data


Next Steps
------------------------------------------------------------------------------
After configuring your databases:

1. Start the MCP server with your configuration
2. Use the ``get_database_schema`` tool to verify your databases are accessible
3. Begin querying your databases through the AI assistant

For more information on available tools and their usage, see the :doc:`todo-add-link` documentation.
