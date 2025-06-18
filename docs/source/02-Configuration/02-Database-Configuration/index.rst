.. _database-configuration:

Database Configuration
==============================================================================
Each database in your configuration represents a separate database connection. This guide explains how to configure individual databases within the :ref:`databases <databases-field>` array.

.. seealso::

    :class:`~mcp_ohmy_sql.config.define.Database` - The configuration class source code for databases


Database Object Structure
------------------------------------------------------------------------------
Each database object has five main fields:

.. code-block:: json

    {
        "identifier": "my_database",
        "description": "Human-readable description",
        "db_type": "sqlite",
        "connection": { ... },
        "schemas": [ ... ]
    }


Identifier Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``identifier`` field is a unique name for your database:

.. code-block:: json

    {
        "identifier": "sales_production"
    }

- **Required**: Yes
- **Type**: String
- **Must be unique**: Across all databases in your configuration
- **Used by**: MCP tools to reference this specific database

**Best Practices:**

- Use descriptive names that indicate purpose and environment
- Examples: ``"sales_prod"``, ``"analytics_dev"``, ``"user_mgmt_staging"``
- Avoid spaces and special characters
- Use underscores or hyphens for readability


Description Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``description`` field provides human-readable context:

.. code-block:: json

    {
        "description": "Production sales database containing customer orders and transactions"
    }

- **Required**: No (defaults to empty string)
- **Type**: String
- **Purpose**: Documentation and understanding

**Examples:**

.. code-block:: json

    {
        "description": "Development SQLite database for testing"
    }

    {
        "description": "Production PostgreSQL warehouse with sales analytics"
    }

    {
        "description": "AWS Redshift cluster for data science workloads"
    }


.. _database-type-field:

Database Type Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``db_type`` field specifies the type of database:

.. code-block:: json

    {
        "db_type": "postgresql"
    }

- **Required**: Yes
- **Type**: String
- **Purpose**: Determines which connection and feature set to use

**Supported Database Types:**

.. literalinclude:: ../../../../mcp_ohmy_sql/constants.py
    :start-after: startdbtypeenum
    :end-before: enddbtypeenum

.. seealso::

    See :class:`~mcp_ohmy_sql.constants.DbTypeEnum` to see full list of supported database types in source code.


Connection Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``connection`` field contains database-specific connection configuration:

.. code-block:: json

    {
        "connection": {
            "type": "sqlalchemy",
            "url": "postgresql://user:password@host:5432/database"
        }
    }

- **Required**: Yes
- **Type**: Object
- **Content**: Varies by database type
- **Purpose**: Defines how to connect to the database

The connection configuration is different for each database type. See :ref:`connection-configuration` for details.


Schemas Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``schemas`` field defines which schemas and tables are accessible:

.. code-block:: json

    {
        "schemas": [
            {
                "name": "public",
                "table_filter": {
                    "include": [],
                    "exclude": ["temp_*"]
                }
            },
            {
                "name": "analytics", 
                "table_filter": {
                    "include": ["sales_*", "customer_*"],
                    "exclude": []
                }
            }
        ]
    }

- **Required**: Yes (but can be an empty array)
- **Type**: Array of schema objects
- **Purpose**: Controls which parts of the database are accessible

See :ref:`schema-configuration` for detailed schema configuration.


Complete Database Examples
------------------------------------------------------------------------------
**SQLite Database:**

.. code-block:: json

    {
        "identifier": "app_dev",
        "description": "Local development database",
        "db_type": "sqlite",
        "connection": {
            "type": "sqlalchemy",
            "url": "sqlite:///./app.db"
        },
        "schemas": [
            {
                "table_filter": {
                    "exclude": ["migrations", "temp_*"]
                }
            }
        ]
    }

.. note::

    SQLITE doesn't need a schema name

**PostgreSQL Database:**

.. code-block:: json

    {
        "identifier": "warehouse_prod",
        "description": "Production data warehouse",
        "db_type": "postgresql",
        "connection": {
            "type": "sqlalchemy",
            "url": "postgresql://analyst:password@warehouse.company.com:5432/analytics",
            "create_engine_kwargs": {
                "pool_size": 5,
                "pool_pre_ping": true
            }
        },
        "schemas": [
            {
                "name": "public",
                "table_filter": {
                    "exclude": ["_temp_*", "staging_*"]
                }
            },
            {
                "name": "reporting",
                "table_filter": {
                    "include": ["sales_summary", "customer_metrics"]
                }
            }
        ]
    }

.. note::

    If you don't specify schema name, then it uses the default schema (usually the public)


Validation Rules
------------------------------------------------------------------------------
When configuring databases, these validation rules apply:

1. **Unique identifiers**: Each database must have a unique ``identifier``
2. **Valid database types**: The ``db_type`` must be one of the supported types
3. **Matching connection types**: The connection configuration must match the database type
4. **Non-empty schemas**: Each database should have at least one schema configured


Next Steps
------------------------------------------------------------------------------
Learn more about specific configuration areas:

- :ref:`schema-configuration` - Configure schemas and table filtering
- :ref:`connection-configuration` - Database connection details
