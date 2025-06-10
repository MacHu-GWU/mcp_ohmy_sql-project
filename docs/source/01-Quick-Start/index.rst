Quick Start Guide
==============================================================================
Welcome to ``mcp_ohmy_sql``! This guide will get you up and running with the SQL Model Context Protocol (MCP) server in just a few minutes.

With ``mcp_ohmy_sql``, you can connect AI assistants and ...:

- Get more familiar with the tables and data
- Explore data and relationships
- Ask business questions in natural language and get answer
- Visualize dataset and entity relationships
- Generate business reports
- Export query results to files


Installation and Setup
------------------------------------------------------------------------------
In this tutorial, we will use `Claude Desktop <https://claude.ai/download>`_ as our AI client.


Step 1. Add the MCP server
------------------------------------------------------------------------------
Following the official `Claude Desktop Manual <https://modelcontextprotocol.io/quickstart/user>`_, we locate the ``claude_desktop_config.json`` file.

- macOS: ``~/Library/Application Support/Claude/claude_desktop_config.json``
- Windows: ``%APPDATA%\Claude\claude_desktop_config.json``

Open it and add the following configuration to the ``mcpServers`` section:

.. code-block:: javascript

    {
        "mcpServers": {
            "OhMySql": {
                "command": "uvx",
                "args": [
                    "--with",
                    "mcp-ohmy-sql[sqlite,postgres]",
                    "mcp-ohmy-sql"
                ],
                "env": {
                    "MCP_OHMY_SQL_CONFIG": "/path/to/mcp_ohmy_sql.json"
                }
            }
        }
    }

Explains:

- We need additional dependencies depends on the database system you are using, the ``mcp-ohmy-sql[sqlite,postgres]`` defines the extra dependencies for SQLite and PostgreSQL. Currently it supports ``sqlite``, ``postgres``, ``mysql``, ``mssql``, ``oracle``.
- The ``MCP_OHMY_SQL_CONFIG`` environment variable points to your configuration file, which defines the databases and their connection settings. You can create it anywhere you like. Please read the :ref:`configuration-guide` for details on how to create this file.


Step 2. Create the Configuration File
------------------------------------------------------------------------------
In this section, we will use a test sqlite database to get you started quickly.

First you can download the `Chinook_sqlite.sqlite <https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_Sqlite.sqlite>`_ file, which is a sample database that contains data about a music store. You can put the ``Chinook_Sqlite.sqlite`` file anywhere you like.

Then create a configuration file named ``mcp_ohmy_sql.json`` using the following content:

.. code-block:: javascript

    {
        "version": "0.1.1",
        "settings": {},
        "databases": [
            {
                "identifier": "chinook sqlite",
                "description": "Chinook is a sample database available for SQL Server, Oracle, MySQL, etc. It can be created by running a single SQL script. Chinook database is an alternative to the Northwind database, being ideal for demos and testing ORM tools targeting single and multiple database servers.",
                "connection": {
                    "type": "sqlalchemy",
                    "create_engine_kwargs": {
                        "url": "sqlite:////path/to/Chinook_Sqlite.sqlite"
                    }
                },
                "schemas": [
                    {
                        "name": null,
                        "table_filter": {
                            "include": [],
                            "exclude": [
                                "Playlist",
                                "PlaylistTrack"
                            ]
                        }
                    }
                ]
            }
        ]
    }

Explains:

- You can put it anywhere you like, but make sure to update the ``MCP_OHMY_SQL_CONFIG`` field in ``claude_desktop_config.json`` to point to the location of your ``mcp_ohmy_sql.json`` file.
- The ``databases.[0].connection.create_engine_kwargs.url`` field should point to the location of your ``Chinook_Sqlite.sqlite`` file. Make sure to use ``sqlite:///{absolute_path_to_your_sqlite_file}`` format.


Step 3. Start the MCP Server
------------------------------------------------------------------------------
Now you can launch your Claude Desktop application, and it will automatically start the MCP server with the configuration you provided.

.. image:: ./01-launch-claude-desktop.png



Trouble Shooting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. image:: ./02-trouble-shooting.png

Problem: uvx command not found

    Solution: Make sure you have installed ``uvx``. Follow the `official guide <https://docs.astral.sh/uv/getting-started/installation/>`_ to install it, and test it with the ``uvx --version`` command. If you didn't install it globally, you can use the absolute path to the ``uvx`` command in the ``claude_desktop_config.json`` file, for xample: ``"command": "/path/to/uvx"``.

    .. code-block:: bash

        pip install uvx


Problem: Claude Desktop cannot connect to the MCP server

    Solution:

    1. make sure the ``mcp_ohmy_sql.json`` format is correct.
    2. make sure the Database connection information in ``mcp_ohmy_sql.json`` is correct, you can test it with the SQLAlchemy directly.

    .. code-block:: python

        import sqlalchemy as sa

        engine = sa.create_engine("db_url_here")
        sql = "SELECT 1"
        with engine.connect() as conn:
            result = conn.execute(sql)
            print(result.fetchone())


Tools
------------------------------------------------------------------------------
For full list of available tools, see the :ref:`tools-guide`.



Usage Example
------------------------------------------------------------------------------



- Get more familiar with the tables and data
- Explore data and relationships
- Ask business questions in natural language and get answer
- Visualize dataset and entity relationships
- Generate business reports
- Export query results to files

1. Get Basic Database Information
------------------------------------------------------------------------------
In this example, we will ask AI to tell us what databases are available to explore.

.. image:: ./11-List-Databases.png



2. Explore data and relationships
------------------------------------------------------------------------------
We want to get more familiar with the table structure and explore important entities, and key relationships in the database.

.. image:: ./12-Get-Database-Schema-Details.png


3. Ask Business Questions in Natural Language
------------------------------------------------------------------------------
We would like to ask AI to answer business questions in natural language. AI then can leverage the database schema information to understand the question, write the SQL, and provide answers.

.. image:: ./13-Ask-Business-Question.png


4. Generate Business Reports
------------------------------------------------------------------------------
Image are easier to consume for human, sometime we would like visualized data report to present, we can ask AI to generate a report for us.

.. image:: ./14-Visualize-Data.png


5. Visualize Dataset and Entity Relationships
------------------------------------------------------------------------------
ER Diagrams are a great way to visualize the relationships between entities in a database. We can ask AI to generate an ER diagram for us, without using any third-party tools.

.. image:: ./15-Visualize-Relationship.png


Next Steps
------------------------------------------------------------------------------
Now that you have ``mcp_ohmy_sql`` running:

1. **Configure Multiple Databases**: Add additional databases to your configuration file
2. **Set Up Table Filters**: Use the filtering system to control which tables are accessible
3. **Optimize Performance**: Configure connection pooling for production databases
4. **Explore Schema Introspection**: Use Claude to understand your database structure
5. **Prepare for Query Execution**: Once available, you'll be ready to run natural language queries

For detailed configuration options and advanced features, continue to the :doc:`../02-Configuration/index` guide.