.. _basic-configuration:

Basic Configuration
==============================================================================
The ``mcp_ohmy_sql`` configuration is a JSON file that defines how the MCP server connects to your databases. This guide introduces the basic structure of the configuration file.

.. warning::

    **Security Warning: Treat Configuration Files as Secrets**

    Your ``mcp_ohmy_sql`` configuration file contains sensitive database credentials including usernames, passwords, connection strings. This file should be treated as a secret and handled with the same security precautions as any other credential file. Never commit configuration files to version control systems, store them in publicly accessible locations, or share them through insecure channels. Ensure the configuration file has appropriate file permissions (600 or 640) to restrict access to authorized users only.

.. seealso::

    :class:`~mcp_ohmy_sql.config.define.Config` - The configuration class source code for mcp_ohmy_sql config


Configuration File Structure
------------------------------------------------------------------------------
Every configuration file has three main sections:

.. code-block:: python

    {
        "version": "0.1.1",
        "settings": {},
        "databases": []
    }


Version Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``version`` field specifies the configuration schema version:

.. code-block:: python

    {
        "version": "0.1.1"
    }

- **Required**: Yes
- **Type**: String
- **Current version**: ``"0.1.1"``

This field ensures compatibility between your configuration and the server version.


Settings Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``settings`` field contains global server configuration:

.. code-block:: python

    {
        "settings": {}
    }

- **Required**: No (defaults to empty object)
- **Type**: Object
- **Current usage**: Reserved for future features

The settings field is currently empty but reserved for future global configuration options such as:

- Query timeout limits
- Result size limits  
- Logging levels
- Performance tuning options


.. _databases-field:

Databases Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``databases`` field contains an array of database configurations:

.. code-block:: python

    {
        "databases": [
            {
                "identifier": "my_first_database",
                "description": "Development SQLite database",
                "db_type": "sqlite",
                "connection": { ... },
                "schemas": [ ... ]
            },
            {
                "identifier": "my_second_database", 
                "description": "Production PostgreSQL database",
                "db_type": "postgresql",
                "connection": { ... },
                "schemas": [ ... ]
            }
        ]
    }

- **Required**: Yes (but can be an empty array)
- **Type**: Array of database objects
- **Purpose**: Defines all databases the MCP server can access

Each database in the array represents a separate database connection with its own configuration, schemas, and access rules.

.. seealso::

    See :ref:`database-configuration` for detailed information on how to configure individual databases.


Complete Basic Example
------------------------------------------------------------------------------
Here's a minimal but complete configuration file:

.. code-block:: python

    {
        "version": "0.1.1",
        "settings": {},
        "databases": [
            {
                "identifier": "app_db",
                "description": "Main application database",
                "db_type": "sqlite",
                "connection": {
                    "type": "sqlalchemy",
                    "url": "sqlite:///./app.db"
                },
                "schemas": [
                    {
                        "name": null,
                        "table_filter": {
                            "include": [],
                            "exclude": []
                        }
                    }
                ]
            }
        ]
    }


Loading Configuration
------------------------------------------------------------------------------
The configuration file is loaded using an environment variable:

.. code-block:: bash

    export MCP_OHMY_SQL_CONFIG=/path/to/your/config.json

When the MCP server starts, it reads this environment variable and loads the configuration from the specified path.


Next Steps
------------------------------------------------------------------------------
Now that you understand the basic structure, learn about:

- :ref:`database-configuration` - How to configure individual databases
- :ref:`schema-configuration` - How to configure database schemas and table filtering
- :ref:`connection-configuration` - How to configure database connections
