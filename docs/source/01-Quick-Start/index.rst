Quick Start Guide
==============================================================================
Welcome to ``mcp_ohmy_sql``! This guide will get you up and running with the SQL Model Context Protocol (MCP) server in just a few minutes.


What is mcp_ohmy_sql?
------------------------------------------------------------------------------
``mcp_ohmy_sql`` is an MCP server that provides AI assistants with secure access to SQL databases. It acts as a bridge between Claude (or other AI models) and your databases, allowing you to:

* Query databases using natural language
* Inspect database schemas and structure
* Export query results to files
* Safely interact with production databases through built-in safeguards

The server uses SQLAlchemy under the hood, supporting virtually any SQL database including PostgreSQL, MySQL, SQLite, Oracle, SQL Server, and more.


Installation
------------------------------------------------------------------------------

Install via pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    pip install mcp-ohmy-sql

Or install from source for development:

.. code-block:: bash

    git clone https://github.com/MacHu-GWU/mcp_ohmy_sql-project.git
    cd mcp_ohmy_sql-project
    pip install -e .


Set Up Configuration
------------------------------------------------------------------------------

Step 1: Create Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create a JSON configuration file to define your database connections. Here's a simple example for a SQLite database:

.. code-block:: json

    {
        "version": "0.1.1",
        "settings": {},
        "databases": [
            {
                "identifier": "my_database",
                "description": "My SQLite database",
                "connection": {
                    "type": "sqlalchemy",
                    "create_engine_kwargs": {
                        "url": "sqlite:///path/to/your/database.db"
                    }
                },
                "schemas": [
                    {
                        "name": null
                    }
                ]
            }
        ]
    }

For more complex setups with multiple databases, PostgreSQL, MySQL, or advanced filtering, see the :doc:`../02-Configuration/index` guide.

Step 2: Set Environment Variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Set the environment variable to point to your configuration file:

.. code-block:: bash

    export MCP_OHMY_SQL_CONFIG=/path/to/your/config.json

Add this to your ``.bashrc``, ``.zshrc``, or equivalent shell configuration file to make it persistent.


Running the MCP Server
------------------------------------------------------------------------------

Start the Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Run the MCP server from the command line:

.. code-block:: bash

    python -m mcp_ohmy_sql.app

The server will start and listen for MCP protocol messages via stdio. You should see output indicating successful startup and database connections.

Connecting to Claude Desktop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To use the MCP server with Claude Desktop, add the following to your Claude Desktop MCP configuration file:

**On macOS**: ``~/Library/Application Support/Claude/claude_desktop_config.json``

**On Windows**: ``%APPDATA%\Claude\claude_desktop_config.json``

.. code-block:: json

    {
        "mcpServers": {
            "mcp_ohmy_sql": {
                "command": "python",
                "args": ["-m", "mcp_ohmy_sql.app"],
                "env": {
                    "MCP_OHMY_SQL_CONFIG": "/path/to/your/config.json"
                }
            }
        }
    }

Restart Claude Desktop to load the new configuration.


How It Works
------------------------------------------------------------------------------

Architecture Overview
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``mcp_ohmy_sql`` server follows a layered architecture:

.. code-block:: text

    Claude Desktop ↔ MCP Protocol ↔ mcp_ohmy_sql Server ↔ SQLAlchemy ↔ Your Databases

1. **MCP Layer** (``tools.py``): Exposes database operations as MCP tools
2. **Configuration Layer** (``config/``): Manages database connections and settings
3. **SQLAlchemy Core** (``sa/``): Handles database operations and schema introspection
4. **Database Layer**: Your actual SQL databases

Available Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Once connected, Claude will have access to these tools:

* **get_database_schema**: Inspect database structure, tables, columns, and relationships
* **execute_query** (coming soon): Run SQL queries with built-in result pagination
* **export_data** (coming soon): Export query results to local files

Configuration System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The configuration system supports:

* **Multiple Databases**: Connect to several databases simultaneously
* **Schema Filtering**: Include/exclude specific tables using patterns
* **Connection Pooling**: Optimize performance with SQLAlchemy engine settings
* **Environment-Specific Configs**: Different settings for dev/staging/production

For detailed configuration options, see :doc:`../02-Configuration/index`.


First Steps with Claude
------------------------------------------------------------------------------

Test Database Connection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Start a conversation with Claude and ask:

.. code-block:: text

    Can you show me the schema of my database?

Claude will use the ``get_database_schema`` tool to retrieve and display your database structure.

Explore Your Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Try these example queries:

.. code-block:: text

    What tables are available in my database?
    
    Show me the structure of the users table.
    
    What are the relationships between my tables?

Natural Language Queries (Coming Soon)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Once query execution is implemented, you'll be able to ask:

.. code-block:: text

    Show me the top 10 customers by order value.
    
    What's the average order amount for each product category?
    
    Export the sales data from last month to a CSV file.


Troubleshooting
------------------------------------------------------------------------------

Common Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Configuration File Not Found**
    * Verify ``MCP_OHMY_SQL_CONFIG`` environment variable is set correctly
    * Check that the file path exists and is readable
    * Ensure the JSON syntax is valid

**Database Connection Failed**
    * Verify your database connection URL is correct
    * Check that required database drivers are installed (e.g., ``psycopg2`` for PostgreSQL)
    * Test the connection outside of the MCP server using SQLAlchemy directly

**MCP Server Not Starting**
    * Check the console output for specific error messages
    * Ensure all dependencies are installed correctly
    * Verify Python version compatibility

**Claude Desktop Not Connecting**
    * Restart Claude Desktop after modifying the configuration
    * Check the Claude Desktop logs for connection errors
    * Verify the MCP server configuration matches your setup exactly

Getting Help
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Check the error messages in the console output
* Review the :doc:`../02-Configuration/index` guide for configuration details
* Submit issues on `GitHub <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/issues>`_


Next Steps
------------------------------------------------------------------------------
Now that you have ``mcp_ohmy_sql`` running:

1. **Configure Multiple Databases**: Add additional databases to your configuration file
2. **Set Up Table Filters**: Use the filtering system to control which tables are accessible
3. **Optimize Performance**: Configure connection pooling for production databases
4. **Explore Schema Introspection**: Use Claude to understand your database structure
5. **Prepare for Query Execution**: Once available, you'll be ready to run natural language queries

For detailed configuration options and advanced features, continue to the :doc:`../02-Configuration/index` guide.