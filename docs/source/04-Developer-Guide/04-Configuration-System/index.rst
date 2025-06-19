.. _configuration-system:

Configuration System: High-Level Architecture
==============================================================================
*Understanding the hierarchical configuration structure that powers the MCP server*


Overview
------------------------------------------------------------------------------
The configuration system is the **foundation of the MCP server** - it defines which databases the server can access, how to connect to them, and which tables/schemas are available for AI interactions. The configuration follows a **hierarchical JSON structure** that maps directly to database organization: Config → Database → Schema → Tables.

This system is designed around **flexibility and security**, supporting multiple database types, complex filtering rules, and various authentication methods while maintaining a consistent interface across all supported database technologies.

**Design Principles**:

- **Hierarchical Structure**: Mirrors real database organization
- **Type Safety**: Pydantic models ensure configuration validity
- **Multi-Database Support**: Single config file manages multiple databases
- **Security-First**: Credential management and access control built-in
- **Extensible**: Easy to add new database types and connection methods

.. seealso::

    `mcp_ohmy_sql/config/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/config>`_


Configuration Hierarchy
------------------------------------------------------------------------------
The configuration system follows a clear three-level hierarchy:

.. code-block:: text

    Config (Root Level)
    ├── version: Configuration schema version
    ├── settings: Global server settings  
    └── databases: List[Database]
        └── Database (Database Level)
            ├── identifier: Unique database ID
            ├── description: Human-readable description
            ├── db_type: Database technology (sqlite, postgresql, aws_redshift)
            ├── connection: Database-specific connection parameters
            └── schemas: List[Schema]
                └── Schema (Schema Level)
                    ├── name: Schema name within database
                    └── table_filter: Include/exclude table patterns

**Configuration Classes**: :class:`~mcp_ohmy_sql.config.define.Config`, :class:`~mcp_ohmy_sql.config.define.Database`, :class:`~mcp_ohmy_sql.config.define.Schema`


Root Level: Config Class
------------------------------------------------------------------------------
**Purpose**: Top-level container that defines the entire MCP server configuration

**Location**: `mcp_ohmy_sql/config/define.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/config/define.py>`_

**Core Responsibilities**:

- Validate configuration schema version compatibility
- Manage global server settings (reserved for future features)
- Coordinate multiple database configurations
- Provide unified configuration loading and validation

**Key Features**:

**Version Management**
    The ``version`` field ensures compatibility between configuration files and server versions, enabling smooth upgrades and preventing configuration mismatches.

**Global Settings**
    The ``settings`` field is currently reserved for future global configuration options like query timeouts, result size limits, and performance tuning parameters.

**Multi-Database Coordination**
  The ``databases`` array allows a single MCP server instance to manage connections to multiple heterogeneous database systems simultaneously.


Database Level: Database Class
------------------------------------------------------------------------------
**Purpose**: Define individual database connections and their metadata

**Location**: `mcp_ohmy_sql/config/define.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/config/define.py>`_

**Core Responsibilities**:

- Specify database technology type (SQLite, PostgreSQL, AWS Redshift, etc.)
- Configure database-specific connection parameters  
- Define which schemas within the database are accessible
- Provide human-readable database descriptions for AI context

**Key Configuration Elements**:

**Database Identification**
  Each database must have a unique ``identifier`` that serves as its reference throughout the system and a ``description`` that provides context for AI interactions.

**Technology Specification**
  The ``db_type`` field determines which database technology is being used, enabling the system to apply appropriate connection logic and SQL dialect handling.

**Connection Configuration**
  Database-specific connection parameters are encapsulated in the ``connection`` field, which varies based on the database type (SQLAlchemy URLs for relational databases, AWS-specific parameters for Redshift).

**Schema Organization**  
  The ``schemas`` array defines which database schemas (or equivalent organizational units) are accessible through the MCP server.


Schema Level: Schema Class
------------------------------------------------------------------------------
**Purpose**: Configure schema-level access control and table filtering

**Location**: `mcp_ohmy_sql/config/define.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/config/define.py>`_

**Core Responsibilities**:
- Define which schema within a database to access
- Implement table inclusion/exclusion filtering rules
- Provide fine-grained access control for database objects
- Support schema-specific configuration overrides

**Key Configuration Elements**:

**Schema Targeting**
    The ``name`` field specifies which schema to access within the database. For databases without explicit schema support (like SQLite), this can be null.

**Table Filtering**
    The ``table_filter`` object enables precise control over which tables are exposed to AI interactions through ``include`` and ``exclude`` pattern lists.

**Security and Access Control**
    Schema-level configuration provides the granular control needed for production deployments where only specific tables should be accessible.


Test Configuration System
------------------------------------------------------------------------------
**Purpose**: Provide comprehensive test environments for development and CI/CD

**Location**: `mcp_ohmy_sql/tests/test_config.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/tests/test_config.py>`_

The test configuration system is **critical infrastructure** that enables comprehensive testing across multiple database technologies. It defines a standardized set of test databases using the same hierarchical configuration structure as production deployments.

**Test Database Coverage**:

**SQLite (Local)**
    Uses local SQLite files for fast, isolated testing without external dependencies. Perfect for unit tests and rapid development cycles.

**PostgreSQL (Container)**  
    Uses local PostgreSQL containers for testing relational database features that require a full SQL engine. Provides realistic database behavior while remaining self-contained.

**AWS Redshift (Real Cloud)**
    Uses actual AWS Redshift Serverless instances for testing cloud-specific functionality, authentication mechanisms, and performance characteristics.

**Configuration Pattern**:

.. code-block:: python

    test_config = Config(
        version="0.1.1",
        settings=Settings(),
        databases=[
            DatabaseEnum.chinook_sqlite,     # Local SQLite
            DatabaseEnum.chinook_postgres,   # Container PostgreSQL  
            DatabaseEnum.chinook_redshift,   # Real AWS Redshift
        ]
    )

**Critical Importance**:

The test configuration object is essential because:

- **MCP Server Tools**: All MCP tools require a valid configuration to establish database connections
- **Integration Testing**: End-to-end tests verify the complete configuration → connection → query pipeline  
- **Multi-Database Validation**: Ensures consistent behavior across different database technologies
- **CI/CD Pipeline**: Automated testing relies on the test configuration for validation


Configuration Loading and Validation
------------------------------------------------------------------------------
**Environment-Based Loading**
    Configuration files are loaded via the ``MCP_OHMY_SQL_CONFIG`` environment variable, enabling different configurations for development, testing, and production environments.

**Pydantic Validation**  
    All configuration classes use Pydantic for automatic validation, type checking, and error reporting, ensuring configuration files are valid before the server starts.

**Error Handling**
    The configuration system provides clear error messages for common configuration mistakes, helping developers quickly identify and fix issues.

**Security Considerations**
    Configuration files contain sensitive credentials and should be treated as secrets with appropriate file permissions and secure handling practices.


Integration with Database Systems
------------------------------------------------------------------------------
The configuration system serves as the **bridge between MCP tools and database systems**:

**Connection Management**
    Configuration objects are used by the adapter layer to establish and manage database connections across different technologies.

**Schema Discovery**
    Database and schema configuration drives the metadata extraction process, determining which database objects are introspected and made available to AI.

**Query Execution**
    Table filtering and access control rules defined in configuration are enforced during query execution to maintain security boundaries.

**Tool Coordination**
    MCP tools use configuration information to provide context-aware responses and ensure they operate within defined access boundaries.


Architecture Benefits
------------------------------------------------------------------------------
**For Development**:

- **Clear Structure**: Hierarchical organization mirrors database concepts
- **Type Safety**: Pydantic validation catches configuration errors early
- **Multi-Environment**: Same configuration pattern works across dev/test/prod
- **Comprehensive Testing**: Test configuration covers all supported database types

**For Operations**:

- **Single Source of Truth**: One configuration file defines all database access
- **Security Control**: Fine-grained access control at schema and table levels
- **Deployment Flexibility**: Environment-based configuration loading
- **Audit Trail**: Configuration changes are trackable and version-controlled

**For AI Integration**:

- **Context Awareness**: Database descriptions provide semantic context to AI
- **Access Boundaries**: Configuration enforces what databases/tables AI can access
- **Multi-Database**: AI can work across different database technologies seamlessly
- **Schema Understanding**: Hierarchical structure helps AI understand database organization


Next Steps
------------------------------------------------------------------------------
The configuration system enables all other MCP server functionality. For detailed configuration examples and connection setup, see the comprehensive :ref:`configuration-guide` documentation which covers:

- Database-specific connection parameters
- Authentication and security configuration  
- Table filtering strategies
- Production deployment patterns
- Troubleshooting configuration issues
