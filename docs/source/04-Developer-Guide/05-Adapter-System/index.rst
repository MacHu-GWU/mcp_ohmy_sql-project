.. _adapters:

Adapters: The Integration Bridge
==============================================================================
*Understanding the adapter layer that connects configuration to database operations and MCP tools*


Overview
------------------------------------------------------------------------------
The MCP server is fundamentally **a collection of tools** that expose database functionality to AI assistants. Each tool combines `configuration settings <configuration-system>`_ with database-specific operations including `SDK utilities <per-sdk-utilities>`_ and the three-layer database metadata system (`models, encoders, extractors <model-encoder-extractor>`_). The `mcp_ohmy_sql/adapter/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/adapter>`_ module serves as the **integration bridge** that connects all these components into cohesive, testable functionality.

At its core, an MCP tool is simply:

.. code-block:: text

    Tool = Configuration + Database Operations (SDK + db/)

The adapter layer orchestrates this combination, ensuring that:

- Configuration objects work seamlessly with database operations
- Different database types are handled consistently  
- 99.9% of the logic can be unit tested without an actual MCP server
- Tool implementations remain pure Python functions

**Design Philosophy**:

- **Pure Functions**: Tools are plain Python functions that can be tested independently
- **Configuration-Driven**: All behavior is controlled by configuration objects
- **Database-Agnostic**: Consistent interface across different database technologies
- **Testable First**: Architecture prioritizes unit testability over MCP integration


Adapter Architecture
------------------------------------------------------------------------------
The adapter system follows a **hierarchical mixin pattern** that separates concerns while enabling code reuse:

.. code-block:: text

    Adapter (Master Class)
    ├── Configuration Management
    ├── RelationalAdapterMixin → db/relational/ + sa/
    ├── AwsRedshiftAdapterMixin → db/aws_redshift/ + aws/aws_redshift/
    ├── MoreAdapterMixin ...
    └── ToolAdapterMixin → MCP Tool Implementations

**Adapter Classes**: :class:`~mcp_ohmy_sql.adapter.adapter.Adapter`, :class:`~mcp_ohmy_sql.adapter.relational_adapter.RelationalAdapterMixin`, :class:`~mcp_ohmy_sql.adapter.aws_redshift_adapter.AwsRedshiftAdapterMixin`, :class:`~mcp_ohmy_sql.adapter.tool_adapter.ToolAdapterMixin`


Master Adapter: adapter.py
------------------------------------------------------------------------------
**Purpose**: Central coordination class that unifies all adapter functionality

**Location**: `mcp_ohmy_sql/adapter/adapter.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/adapter/adapter.py>`_

**Core Responsibilities**:

- Hold the configuration object that defines all database access
- Coordinate between different database adapter mixins
- Provide common functionality like database/schema object retrieval
- Serve as the single entry point for all MCP tool operations

**Key Features**:

**Configuration Integration**
    The adapter wraps a :class:`~mcp_ohmy_sql.config.define.Config` object and makes it available to all mixins, enabling configuration-driven behavior throughout the system.

**Database Resolution**
    The :meth:`~mcp_ohmy_sql.adapter.adapter.Adapter.get_database_and_schema_object()` method provides safe access to configuration objects with comprehensive error handling and validation.

**Mixin Coordination**
    By inheriting from multiple mixins, the adapter combines database-specific operations with tool implementations in a single cohesive interface.


Per-Database Adapters
------------------------------------------------------------------------------
Each supported database technology has its own adapter mixin that bridges configuration objects with the corresponding database operations:

- `mcp_ohmy_sql/adapter/relational_adapter.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/adapter/relational_adapter.py>`_
- `mcp_ohmy_sql/adapter/aws_redshift_adapter.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/adapter/aws_redshift_adapter.py>`_


Tool Implementation: tool_adapter.py
------------------------------------------------------------------------------
**Purpose**: Implement MCP tool logic using configuration and database adapters

**Location**: `mcp_ohmy_sql/adapter/tool_adapter.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/adapter/tool_adapter.py>`_

**Core Responsibility**: Provide the actual MCP tool implementations as **pure Python functions** that can be tested independently of the MCP server infrastructure.

.. seealso::

    **Tool Functions**: :ref:`tools-guide`

**Key Design Benefits**:

**Pure Functions**
    All tools are implemented as instance methods that take simple parameters and return strings, making them easy to test and debug.

**Database Abstraction**
    Tools provide a consistent interface regardless of the underlying database technology.

**Configuration-Driven**
    All tool behavior is controlled by the configuration object, enabling different environments and setups without code changes.

**Performance Monitoring**
    Tools like ``execute_select_statement`` include timing information to help optimize query performance.


Testing Strategy: Pure Functions First
------------------------------------------------------------------------------
The adapter architecture is specifically designed to **maximize unit testability**:

**Why This Matters**:

Traditional MCP server testing requires:

- Full MCP server startup
- Complex mock configurations  
- Integration test overhead
- Difficult debugging

The adapter approach enables:

- Direct function testing with simple inputs
- Fast unit tests without MCP overhead
- Easy mocking of database connections
- Clear separation of concerns

**Testing Pattern**:

.. code-block:: python

    # Direct adapter testing - no MCP server required
    def test_tool_list_databases():
        config = create_test_config()
        adapter = Adapter(config=config)
        
        result = adapter.tool_list_databases()
        
        assert "chinook_sqlite" in result
        assert "db_type=sqlite" in result

**Test Coverage**: The adapter layer has comprehensive unit tests at `tests/adapter/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/tests/adapter>`_ that verify:

- Configuration integration works correctly
- Database-specific operations are called properly  
- Tool outputs match expected formats
- Error handling provides meaningful messages


Integration Flow: Configuration to Tool Output
------------------------------------------------------------------------------
Here's how a complete tool request flows through the adapter system:

**1. Tool Invocation**:
User requests schema details for a database

**2. Configuration Resolution**:
Adapter resolves database and schema objects from configuration

**3. Database Operations**:
Appropriate database adapter is called based on database type

**4. SDK Integration**:
Database adapter uses SDK utilities (SQLAlchemy, boto3, etc.)

**5. Metadata Extraction**:
Database-specific extractors pull schema information  

**6. Model Creation**:
Raw metadata is structured into typed model objects

**7. Encoding**:
Models are encoded into AI-friendly text format

**8. Tool Response**:
Formatted result is returned to the MCP client

**Complete Flow Example**:

.. code-block:: text

    User: "Get schema for chinook_sqlite"
    ↓
    tool_get_schema_details(database_identifier="chinook_sqlite")
    ↓  
    get_database_and_schema_object() → finds Database + Schema objects
    ↓
    get_relational_schema_info() → calls db/relational/new_schema_info()
    ↓
    SQLAlchemy engine + metadata → sa/ utilities → db extraction
    ↓
    Models → Encoders → AI-friendly schema text
    ↓
    "Schema default(Table Album(AlbumId:INT*PK, Title:STR*NN, ...))"


Architecture Benefits
------------------------------------------------------------------------------
**For Development**:

- **Independent Testing**: 99.9% of logic can be unit tested without MCP server
- **Clear Boundaries**: Each adapter has well-defined responsibilities
- **Database Flexibility**: Easy to add new database types by adding mixins
- **Debug Friendly**: Pure functions are easy to test and troubleshoot

**For Operations**:

- **Configuration Control**: All behavior controlled by configuration files
- **Performance Monitoring**: Built-in timing for query performance optimization  
- **Error Handling**: Comprehensive error messages for troubleshooting
- **Multi-Database**: Single interface for heterogeneous database environments

**For AI Integration**:

- **Consistent Interface**: Same tool behavior across all database types
- **Rich Context**: Tools provide detailed schema information for accurate SQL generation
- **Performance Awareness**: Execution timing helps guide query optimization
- **Access Control**: Configuration-based filtering enforces security boundaries

The adapter layer is where **configuration meets capability** - transforming static configuration into dynamic database interactions while maintaining the testability and clarity that makes the system maintainable and reliable.
