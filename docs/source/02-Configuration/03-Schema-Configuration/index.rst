.. _schema-configuration:

Schema Configuration
==============================================================================
Schemas define which parts of your database are accessible through the MCP server. Each database can have multiple schemas, and each schema can have its own table filtering rules.

.. seealso::

    :class:`~mcp_ohmy_sql.config.define.Config` - The configuration class source code for schema


Schema Object Structure
------------------------------------------------------------------------------
Each schema object has two main fields:

.. code-block:: python

    {
        "name": "schema_name",
        "table_filter": {
            "include": [],
            "exclude": []
        }
    }


Schema Name Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``name`` field specifies which database schema to use:

.. code-block:: python

    {
        "name": "public"
    }

- **Required**: No (defaults to ``null``), if omitted, uses the database's default schema when possible
- **Type**: String or ``null``
- **Purpose**: Identifies the database schema

**Special Cases:**

.. code-block:: python

    {
        "name": null
    }

When ``name`` is ``null`` or omitted, the database's default schema is used:

- **SQLite**: No explicit schemas (always uses default)
- **PostgreSQL**: Uses ``"public"`` schema by default
- **MySQL**: Uses the database name as schema
- **SQL Server**: Uses ``"dbo"`` schema by default

**Multiple Schemas Example:**

.. code-block:: python

    {
        "schemas": [
            {
                "name": "public",
                "table_filter": { ... }
            },
            {
                "name": "analytics", 
                "table_filter": { ... }
            },
            {
                "name": "reporting",
                "table_filter": { ... }
            }
        ]
    }


Table Filter Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``table_filter`` field controls which tables within the schema are accessible by the MCP server:

.. code-block:: python

    {
        "table_filter": {
            "include": ["users", "orders", "products"],
            "exclude": ["temp_*", "backup_*"]
        }
    }

- **Required**: No (defaults to empty include/exclude lists)
- **Type**: Object with ``include`` and ``exclude`` arrays
- **Purpose**: Fine-grained control over table access


Include Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``include`` array specifies which tables to make accessible:

.. code-block:: python

    {
        "include": ["users", "orders", "products"]
    }

- **Type**: Array of strings
- **Behavior**: If empty, includes all tables (except those in exclude list)
- **Supports wildcards**: Use ``*`` for pattern matching

**Wildcard Examples:**

.. code-block:: python

    {
        "include": [
            "sales_*",      # All tables starting with "sales_"
            "*_summary",    # All tables ending with "_summary"
            "fact_*",       # All fact tables
            "dim_*"         # All dimension tables
        ]
    }


Exclude Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``exclude`` array specifies which tables to hide:

.. code-block:: python

    {
        "exclude": ["temp_*", "backup_*", "migrations"]
    }

- **Type**: Array of strings
- **Behavior**: Always excludes matching tables, even if they match include patterns
- **Supports wildcards**: Use ``*`` for pattern matching

**Common Exclude Patterns:**

.. code-block:: python

    {
        "exclude": [
            "temp_*",             # Temporary tables
            "staging_*",          # Staging tables
            "_*",                 # Tables starting with underscore
            "*_backup",           # Backup tables
            "pg_*",               # PostgreSQL system tables
            "information_schema", # Standard SQL system schema
            "sys_*",              # System tables
            "mysql_*"             # MySQL system tables
        ]
    }


Filter Logic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The filtering logic works as follows:

1. **Include first**: If ``include`` is not empty, only listed tables are considered
2. **Exclude second**: Tables in ``exclude`` are removed, even if they were included
3. **Default behavior**: If ``include`` is empty, all tables are included initially

**Examples:**

.. code-block:: python

    # Include everything except temporary tables
    {
        "include": [],
        "exclude": ["temp_*", "staging_*"]
    }

    # Only include specific tables
    {
        "include": ["users", "orders", "products"],
        "exclude": []
    }

    # Include sales tables but exclude backups
    {
        "include": ["sales_*"],
        "exclude": ["*_backup", "*_temp"]
    }


Complete Schema Examples
------------------------------------------------------------------------------
**Default Schema with Basic Filtering:**

.. code-block:: python

    {
        "schemas": [
            {
                "name": null,
                "table_filter": {
                    "include": [],
                    "exclude": ["migrations", "temp_*", "_*"]
                }
            }
        ]
    }

**Multiple Schemas with Different Rules:**

.. code-block:: python

    {
        "schemas": [
            {
                "name": "public",
                "table_filter": {
                    "include": [],
                    "exclude": ["temp_*", "backup_*"]
                }
            },
            {
                "name": "analytics",
                "table_filter": {
                    "include": ["fact_*", "dim_*", "*_summary"],
                    "exclude": ["*_staging"]
                }
            },
            {
                "name": "reporting",
                "table_filter": {
                    "include": ["sales_report", "customer_metrics", "product_performance"],
                    "exclude": []
                }
            }
        ]
    }

**Data Warehouse Schema Organization:**

.. code-block:: python

    {
        "schemas": [
            {
                "name": "raw",
                "table_filter": {
                    "include": [],
                    "exclude": ["*_temp", "*_staging", "*_test"]
                }
            },
            {
                "name": "transformed",
                "table_filter": {
                    "include": ["clean_*", "enriched_*"],
                    "exclude": ["*_backup"]
                }
            },
            {
                "name": "marts",
                "table_filter": {
                    "include": ["*_mart", "*_summary", "*_metrics"],
                    "exclude": []
                }
            }
        ]
    }


Best Practices
------------------------------------------------------------------------------
**Security:**

- Always exclude sensitive tables (user passwords, tokens, etc.)
- Use specific include lists for production environments
- Exclude system and administrative tables

.. code-block:: python

    {
        "exclude": [
            "user_passwords",
            "api_tokens", 
            "admin_*",
            "audit_*"
        ]
    }

**Performance:**

- Exclude large temporary or staging tables
- Filter out tables not needed for analysis
- Consider excluding tables with frequent schema changes

.. code-block:: python

    {
        "exclude": [
            "temp_*",
            "staging_*", 
            "log_*",
            "*_archive"
        ]
    }

**Organization:**

- Group related tables in schemas
- Use consistent naming patterns
- Document your filtering strategy

.. code-block:: python

    {
        "name": "analytics",
        "table_filter": {
            "include": ["fact_*", "dim_*", "agg_*"],
            "exclude": ["*_temp", "*_staging"]
        }
    }


Common Patterns
------------------------------------------------------------------------------
**Development Environment:**

.. code-block:: python

    {
        "schemas": [
            {
                "name": null,
                "table_filter": {
                    "include": [],
                    "exclude": ["test_*", "temp_*", "migrations"]
                }
            }
        ]
    }

**Production Environment:**

.. code-block:: python

    {
        "schemas": [
            {
                "name": "public",
                "table_filter": {
                    "include": ["users", "orders", "products", "analytics_*"],
                    "exclude": ["*_backup", "*_temp", "*_staging", "admin_*"]
                }
            }
        ]
    }

**Analytics Environment:**

.. code-block:: python

    {
        "schemas": [
            {
                "name": "warehouse",
                "table_filter": {
                    "include": ["fact_*", "dim_*", "*_summary", "*_metrics"],
                    "exclude": ["*_raw", "*_staging", "*_temp"]
                }
            }
        ]
    }


Next Steps
------------------------------------------------------------------------------
Now that you understand schema configuration, learn about:

- :ref:`connection-configuration` - How to configure database connections
