.. _connection-configuration:

Connection Configuration
==============================================================================
The connection configuration is the most important part of your database setup. It defines how the MCP server connects to your specific database system. Each database type (:ref:`db_type <database-type-field>`) requires a different connection configuration.


Connection Types Overview
------------------------------------------------------------------------------
The ``mcp_ohmy_sql`` server supports different connection types based on your database system:

.. code-block:: python

    {
        "connection": {
            "type": "connection_type_name",
            # ... type-specific configuration
        }
    }

The ``type`` field determines which connection handler to use, and each type has its own specific configuration options.


Supported Connection Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**SQLAlchemy-based Connections** (``"sqlalchemy"``)

Used for traditional relational databases:

- SQLite
- PostgreSQL  
- MySQL/MariaDB
- Microsoft SQL Server
- Oracle

.. code-block:: python

    {
        "db_type": "postgresql",
        "connection": {
            "type": "sqlalchemy",
            "url": "postgresql://user:password@host:5432/database"
        }
    }

**AWS Redshift Connections** (``"aws_redshift"``)

Used for Amazon Redshift data warehouses:

.. code-block:: python

    {
        "db_type": "aws_redshift", 
        "connection": {
            "type": "aws_redshift",
            "method": "sqlalchemy",
            "cluster_identifier": "my-cluster",
            "database": "warehouse"
        }
    }

**Future Connection Types**

Planned support for additional database systems:

- ``"mongodb"`` - MongoDB with SQL interface
- ``"elasticsearch"`` - Elasticsearch SQL
- ``"opensearch"`` - OpenSearch SQL  
- ``"snowflake"`` - Snowflake cloud database
- ``"duckdb"`` - DuckDB analytical database


Database Type to Connection Type Mapping
------------------------------------------------------------------------------
Each ``db_type`` uses a specific connection type:

.. list-table:: Database Type Mapping
   :header-rows: 1
   :widths: 25 25 50

   * - Database Type
     - Connection Type
     - Documentation
   * - ``sqlite``
     - ``sqlalchemy``
     - :ref:`relational-database-connection-configuration`
   * - ``postgresql``
     - ``sqlalchemy``  
     - :ref:`relational-database-connection-configuration`
   * - ``mysql``
     - ``sqlalchemy``
     - :ref:`relational-database-connection-configuration`
   * - ``mssql``
     - ``sqlalchemy``
     - :ref:`relational-database-connection-configuration`
   * - ``oracle``
     - ``sqlalchemy``
     - :ref:`relational-database-connection-configuration`
   * - ``aws_redshift``
     - ``aws_redshift``
     - :ref:`aws-redshift-connection-configuration`


Connection Configuration Structure
------------------------------------------------------------------------------
The connection object always starts with a ``type`` field, followed by type-specific configuration:

**SQLAlchemy Connection Structure:**

.. code-block:: python

    {
        "connection": {
            "type": "sqlalchemy",
            "url": "database_connection_string",
            "create_engine_kwargs": {
                # Optional SQLAlchemy engine parameters
            }
        }
    }

**AWS Redshift Connection Structure:**

.. code-block:: python

    {
        "connection": {
            "type": "aws_redshift",
            "method": "sqlalchemy",
            # Authentication method 1: Direct credentials
            "host": "cluster.region.redshift.amazonaws.com",
            "port": 5439,
            "database": "warehouse",
            "username": "user",
            "password": "password",
            
            # OR Authentication method 2: IAM-based
            "cluster_identifier": "my-cluster",
            "database": "warehouse", 
            "boto_session_kwargs": {
                "region_name": "us-east-1",
                "profile_name": "default"
            }
        }
    }


Common Configuration Patterns
------------------------------------------------------------------------------
**Development Environment:**

Simple local databases for development:

.. code-block:: python

    {
        "identifier": "dev_db",
        "db_type": "sqlite",
        "connection": {
            "type": "sqlalchemy",
            "url": "sqlite:///./dev.db"
        }
    }

**Production Environment:**

Production databases with connection pooling and optimization:

.. code-block:: python

    {
        "identifier": "prod_postgres",
        "db_type": "postgresql", 
        "connection": {
            "type": "sqlalchemy",
            "url": "postgresql://user:password@prod-host:5432/database",
            "create_engine_kwargs": {
                "pool_size": 10,
                "max_overflow": 20,
                "pool_pre_ping": true,
                "pool_recycle": 3600
            }
        }
    }

**Cloud Data Warehouse:**

AWS Redshift with IAM authentication:

.. code-block:: python

    {
        "identifier": "analytics_warehouse",
        "db_type": "aws_redshift",
        "connection": {
            "type": "aws_redshift", 
            "method": "sqlalchemy",
            "cluster_identifier": "analytics-cluster",
            "database": "warehouse",
            "boto_session_kwargs": {
                "region_name": "us-east-1",
                "profile_name": "analytics"
            }
        }
    }


Security Considerations
------------------------------------------------------------------------------
**Credential Management:**

Never store passwords directly in configuration files:

.. code-block:: python

    # ❌ Don't do this
    {
        "url": "postgresql://user:mypassword123@host:5432/db"
    }

    # ✅ Use environment variables instead
    {
        "url": "postgresql://user:${DB_PASSWORD}@host:5432/db"
    }

**Best Practices:**

1. **Use environment variables** for sensitive data
2. **Use IAM authentication** when available (AWS, GCP, Azure)
3. **Limit database user permissions** to read-only when possible
4. **Use SSL/TLS connections** for remote databases
5. **Store configuration files securely** with proper file permissions

**AWS Redshift IAM Example:**

.. code-block:: python

    {
        "connection": {
            "type": "aws_redshift",
            "method": "sqlalchemy", 
            "cluster_identifier": "my-cluster",
            "database": "warehouse",
            "boto_session_kwargs": {
                "region_name": "us-east-1",
                # Uses AWS credentials from environment, IAM roles, or profiles
                # No hardcoded passwords needed
            }
        }
    }


Troubleshooting Connection Issues
------------------------------------------------------------------------------
**Common Connection Problems:**

1. **Invalid connection strings**: Check URL format and parameters
2. **Network connectivity**: Verify host, port, and firewall rules  
3. **Authentication failures**: Check username, password, and permissions
4. **Missing database drivers**: Install required Python packages
5. **SSL/TLS issues**: Configure SSL settings properly

**Testing Connections:**

You can test your connection configuration using SQLAlchemy directly:

.. code-block:: python

    from sqlalchemy import create_engine
    
    # Test your connection URL
    engine = create_engine("postgresql://user:password@host:5432/db")
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print(result.fetchone())

**Error Messages:**

The MCP server provides detailed error messages for connection failures:

- **File access errors**: Check configuration file path and permissions
- **JSON parsing errors**: Validate JSON syntax
- **Configuration validation errors**: Check required fields and types
- **Database connection errors**: Verify connection parameters and network access


Next Steps
------------------------------------------------------------------------------
Learn about specific connection types:

- :ref:`relational-database-connection-configuration` - SQLAlchemy-based database connections
- :ref:`aws-redshift-connection-configuration` - AWS Redshift connection configuration
