.. _relational-database-connection-configuration:

Relational Database Connection Configuration
==============================================================================
For traditional relational databases, ``mcp_ohmy_sql`` uses `SQLAlchemy <https://www.sqlalchemy.org/>`_ as the underlying connection library. This provides robust, well-tested connectivity to all major SQL databases.

.. seealso::

    :class:`~mcp_ohmy_sql.config.sqlalchemy.SqlalchemyConnection` - The configuration class source code for SqlAlchemy connection


SQLAlchemy Connection Type
------------------------------------------------------------------------------
Relational databases use the ``"sqlalchemy"`` connection type:

.. code-block:: python

    {
        "connection": {
            "type": "sqlalchemy",
            "url": "database_connection_string",
            "create_engine_kwargs": {}
        }
    }


Supported Databases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SQLAlchemy supports a `wide range of relational databases <https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls>`_:

.. list-table:: Supported Relational Databases
   :header-rows: 1
   :widths: 20 20 60

   * - Database
     - ``db_type``
     - Connection URL Format
   * - SQLite
     - ``"sqlite"``
     - ``sqlite:///path/to/database.db``
   * - PostgreSQL
     - ``"postgresql"``
     - ``postgresql://user:password@host:port/database``
   * - MySQL
     - ``"mysql"``
     - ``mysql://user:password@host:port/database``
   * - Microsoft SQL Server
     - ``"mssql"``
     - ``mssql+pyodbc://user:password@host:port/database``
   * - Oracle
     - ``"oracle"``
     - ``oracle+oracledb://user:password@host:port/database``


Connection URL
------------------------------------------------------------------------------
The most important field is the ``url``, which specifies how to connect to your database:

.. code-block:: python

    {
        "connection": {
            "type": "sqlalchemy",
            "url": "postgresql://analyst:password@warehouse.company.com:5432/analytics"
        }
    }

**URL Format:**

The connection URL follows this pattern:

.. code-block::

    dialect+driver://username:password@host:port/database?param1=value1&param2=value2

**URL Components:**

- **dialect**: Database type (``postgresql``, ``mysql``, ``sqlite``, etc.)
- **driver**: Python database driver (optional, uses default if omitted)
- **username**: Database username
- **password**: Database password  
- **host**: Database server hostname or IP address
- **port**: Database server port number
- **database**: Database/schema name
- **parameters**: Additional connection parameters (optional)


SQLAlchemy Engine Configuration
------------------------------------------------------------------------------
The ``create_engine_kwargs`` field allows you to pass additional parameters to SQLAlchemy's `create_engine() <https://docs.sqlalchemy.org/en/20/core/engines.html>`_ function:

.. code-block:: python

    {
        "connection": {
            "type": "sqlalchemy",
            "url": "postgresql://user:password@host:5432/database",
            "create_engine_kwargs": {
                "pool_size": 10,
                "max_overflow": 20,
                "pool_pre_ping": true,
                "pool_recycle": 3600,
                "echo": false
            }
        }
    }

.. tip::

    Read the `sqlalchemy.create_engine() <https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine>`_ official documentation for a full list of available parameters.

**Production Configuration Example:**

.. code-block:: python

    {
        "connection": {
            "type": "sqlalchemy",
            "url": "postgresql://user:password@host:5432/database", 
            "create_engine_kwargs": {
                "pool_size": 5,
                "max_overflow": 10,
                "pool_pre_ping": true,
                "pool_recycle": 3600,
                "echo": false,
                "connect_args": {
                    "sslmode": "require",
                    "connect_timeout": 10
                }
            }
        }
    }


Alternative Connection Methods
------------------------------------------------------------------------------
Instead of providing a complete URL, you can specify connection components separately:

.. code-block:: python

    {
        "connection": {
            "type": "sqlalchemy",
            "drivername": "postgresql+psycopg2",
            "username": "analyst",
            "password": "password",
            "host": "warehouse.company.com", 
            "port": 5432,
            "database": "analytics",
            "query": {
                "sslmode": "require"
            }
        }
    }

This approach when your database credentials contain special characters (such as ``@``, ``:``, ``/``, ``%``, etc.) that need URL encoding, we recommend using the separate parameter approach instead of embedding credentials directly in the URL string. The ``SqlalchemyConnection`` class provides individual fields that automatically handle character escaping for you.

Benefits of this approach:

- **Automatic escaping**: No need to manually URL-encode special characters
- **Better readability**: Credentials are clearly separated and easier to read
- **Reduced errors**: Eliminates common URL encoding mistakes


Database Drivers
------------------------------------------------------------------------------
SQLAlchemy requires appropriate database drivers to be installed. If you need to use a specific database driver that's not included by default, you can specify it in the ``drivername`` field. However, make sure to install the required Python package by adding it to your MCP configuration in your AI client using ``uv --with``:

For more information on installing additional Python packages with your MCP server, please refer to [TODO, I will add later] section.


Troubleshooting
------------------------------------------------------------------------------
**Common Issues:**

1. **Driver not installed**: Install the appropriate database driver in your MCP client configuration
2. **Connection refused**: Check host, port, and firewall settings
3. **Authentication failed**: Verify username and password
4. **SSL errors**: Configure SSL parameters correctly
5. **Pool exhaustion**: Adjust pool_size and max_overflow settings

**Testing Your Connection:**

You can test your SQLAlchemy connection URL independently:

.. code-block:: python

    from sqlalchemy import create_engine, text
    
    # Test the connection
    url = "postgresql://user:password@host:5432/database"
    engine = create_engine(url)
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        print(result.fetchone())


SQLAlchemy Documentation
------------------------------------------------------------------------------
For comprehensive information about SQLAlchemy connection configuration, refer to the official SQLAlchemy documentation:

- `SQLAlchemy Engine Configuration <https://docs.sqlalchemy.org/en/20/core/engines.html>`_
- `SQLAlchemy Database URLs <https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls>`_
- `SQLAlchemy Connection Pooling <https://docs.sqlalchemy.org/en/20/core/pooling.html>`_
- `SQLAlchemy Dialects <https://docs.sqlalchemy.org/en/20/dialects/index.html>`_

The ``mcp_ohmy_sql`` server leverages SQLAlchemy's full feature set, so all SQLAlchemy configuration options are available through the ``create_engine_kwargs`` field.


Next Steps
------------------------------------------------------------------------------
- :ref:`aws-redshift-connection-configuration` - Configure AWS Redshift connections
- :ref:`schema-configuration` - Set up schema and table filtering
- :ref:`basic-configuration` - Return to basic configuration overview
