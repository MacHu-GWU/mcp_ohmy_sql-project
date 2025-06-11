Source Code Structure Guide
==============================================================================
*A comprehensive guide for contributors to understand the architectural design patterns and code organization of the mcp_ohmy_sql project.*


Overview
------------------------------------------------------------------------------
This document explains the architectural design patterns used in `mcp_ohmy_sql <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql>`_ to help contributors understand how the codebase is organized and how to extend it effectively. The project follows a layered, modular architecture that promotes separation of concerns, testability, and maintainability.


Core Design Philosophy
------------------------------------------------------------------------------
The mcp_ohmy_sql project is built around three fundamental principles:

1. **Separation of Concerns**: Each subsystem (SQLAlchemy, AWS, Elasticsearch, DuckDB, etc.) operates independently without cross-dependencies
2. **Integration Layer**: A central hub module provides controlled integration between subsystems and configuration
3. **Testability**: The architecture allows easy unit testing without requiring a full MCP server setup


Architectural Layers
------------------------------------------------------------------------------
The codebase is organized into distinct layers, each with specific responsibilities:

.. code-block:: text

    User Request → MCP Client → tools.py → hub/tool_hub → hub → subsystem packages → Database/Service


Layer 1: Entry Point (config/)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Purpose**: Configuration management and application bootstrapping

**Location**: `mcp_ohmy_sql/config/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/config>`_

**Responsibilities**:

- Load and validate configuration from environment variables
- Parse JSON configuration files
- Provide configuration objects to other layers
- Manage database connection parameters
- Handle multi-database, multi-schema configurations

**Key Files**:

- `config_define.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/config/config_define.py>`_: Core configuration classes and database definitions
- `config_init.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/config/config_init.py>`_: Configuration loading and initialization logic

**Design Pattern**: The config layer acts as the single source of truth for all application settings and serves as the entry point for the entire system.


Layer 2: Subsystem Packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Purpose**: Domain-specific tool implementations

**Locations**: 

- `mcp_ohmy_sql/sa/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/sa>`_ (SQLAlchemy tools)
- `mcp_ohmy_sql/aws/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/aws>`_ (AWS tools - future)
- `mcp_ohmy_sql/elasticsearch/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/elasticsearch>`_ (Elasticsearch tools - future)
- `mcp_ohmy_sql/duckdb/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/duckdb>`_ (DuckDB tools - future)

**Responsibilities**:

- Implement domain-specific functionality
- Provide focused, single-responsibility tools
- Maintain no dependencies on other subsystem packages
- Handle subsystem-specific error conditions
- Expose clean, well-documented APIs

**Key Principles**:

- **Independence**: Each subsystem package can be developed, tested, and maintained separately
- **Focus**: Each package handles only its specific domain (database type, cloud service, etc.)
- **Reusability**: Subsystem tools can be used independently of the MCP context

**Example Structure** (SQLAlchemy subsystem):

.. code-block:: text

    sa/
    ├── __init__.py          # Package initialization and public API
    ├── api.py               # Public API exports
    ├── metadata.py          # Database schema introspection
    ├── query.py             # Query execution functionality  
    ├── schema_encoder.py    # LLM-friendly schema encoding
    └── types.py             # Type definitions and mappings

Layer 3: Integration Layer (hub/)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Purpose**: Coordinate between configuration and subsystem packages

**Location**: `mcp_ohmy_sql/hub/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/hub>`_

**Responsibilities**:

- Bridge configuration objects with subsystem implementations
- Manage cross-subsystem interactions
- Handle resource lifecycle (connections, sessions, etc.)
- Provide unified error handling and logging
- Coordinate complex operations that span multiple subsystems

**Design Pattern**: The hub acts as an integration facade, presenting a unified interface while managing the complexity of coordinating multiple subsystems.

**Key Benefits**:

- Subsystems remain decoupled from each other
- Configuration changes don't directly impact subsystem code
- Complex workflows can be orchestrated without tight coupling
- Easy to add new subsystems without modifying existing ones


Layer 4: MCP Tool Implementation (hub/tool_hub)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Purpose**: Low-level MCP tool implementations

**Location**: `mcp_ohmy_sql/hub/tool_hub.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/hub/tool_hub.py>`_

**Responsibilities**:

- Implement MCP-specific tool logic
- Handle MCP protocol requirements (serialization, error formats, etc.)
- Coordinate calls to hub integration layer
- Manage tool-specific validation and error handling
- Provide tool metadata and documentation

**Design Benefits**:

- MCP-specific concerns are isolated from business logic
- Tools can be thoroughly unit tested without MCP server overhead
- Easy to modify MCP behavior without affecting core functionality
- Clear separation between tool interface and implementation


Layer 5: MCP Tool Wrapper (tools.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Purpose**: Thin wrapper exposing tools to MCP server

**Location**: `mcp_ohmy_sql/tools.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/tools.py>`_

**Responsibilities**:

- Register MCP tools with FastMCP server
- Provide tool decorators and metadata
- Forward requests to tool_hub implementations
- Handle MCP server integration

**Example Implementation**:

.. dropdown:: tools.py

    .. literalinclude:: ../../../mcp_ohmy_sql/tools.py
        :language: python
        :emphasize-lines: 1-1
        :linenos:

**Design Benefits**:

- Minimal code in the MCP interface layer
- Easy to add/remove tools without complex changes
- Tool logic remains testable independently of MCP
- Clear separation of MCP concerns from business logic


Data Flow Example
------------------------------------------------------------------------------
Here's how a typical request flows through the architecture:

1. **User Request**: "Get schema details for database 'chinook_sqlite'"

2. **MCP Layer** (``tools.py``):
    - ``get_schema_details()`` receives the request
    - Forwards to ``tool_hub.tool_get_schema_details()``

3. **Tool Implementation** (``hub/tool_hub``):
    - Validates the database identifier
    - Calls hub integration layer with processed parameters

4. **Integration Layer** (``hub/``):
    - Retrieves configuration for the specified database
    - Initializes appropriate subsystem (SQLAlchemy in this case)
    - Coordinates the schema retrieval operation

5. **Subsystem Layer** (``sa/``):
    - Connects to the database using provided configuration
    - Performs schema introspection using SQLAlchemy metadata
    - Encodes schema information in LLM-friendly format

6. **Response Path**: Results flow back through the same layers in reverse


Benefits of This Architecture
------------------------------------------------------------------------------
**For Contributors**:

- Clear boundaries make it easy to understand where to add new functionality
- Subsystems can be developed and tested independently  
- Integration layer provides consistent patterns for new subsystems
- MCP tools follow predictable patterns

**For Maintainability**:

- Changes to one subsystem don't affect others
- Configuration changes are centralized and controlled
- Easy to add support for new database types or cloud services
- Clear separation of concerns reduces complexity

**For Testing**:

- Each layer can be unit tested independently
- Mock objects can be easily substituted at layer boundaries
- Integration tests can focus on specific layer interactions
- No need for full MCP server to test business logic


Adding New Functionality
------------------------------------------------------------------------------


Extending a Subsystem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To add new functionality to an existing subsystem (e.g., SQLAlchemy):

1. Add the core implementation to the appropriate ``sa/`` module
2. Update ``sa/api.py`` to export new functionality
3. Add integration logic to ``hub/`` if needed
4. Implement MCP tool in ``hub/tool_hub.py``
5. Add wrapper function to ``tools.py``
6. Write unit tests for each layer


Adding a New Subsystem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To add support for a new service (e.g., AWS):

1. Create new package: ``mcp_ohmy_sql/aws/``
2. Implement service-specific functionality following the ``sa/`` pattern
3. Add integration logic to ``hub/`` for coordinating with config
4. Implement MCP tools in ``hub/tool_hub.py``
5. Add wrapper functions to ``tools.py``
6. Update configuration schema to support new subsystem
7. Write comprehensive test suite


Adding New MCP Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To add a new MCP tool:

1. Implement core logic in appropriate subsystem package
2. Add coordination logic to ``hub/`` if needed
3. Implement tool in ``hub/tool_hub.py`` with proper error handling
4. Add wrapper function to ``tools.py`` with ``@mcp.tool()`` decorator
5. Write unit tests covering all layers
6. Update documentation


Code Organization Guidelines
------------------------------------------------------------------------------
**File Naming Conventions**:

- Use descriptive names that clearly indicate purpose
- Group related functionality in modules
- Keep modules focused on single responsibilities

**Import Patterns**:

- Subsystem packages should only import from ``constants.py`` and ``utils.py``
- Hub modules can import from config and subsystem packages
- Tool implementations import from hub modules
- Avoid circular dependencies

**Error Handling**:

- Each layer should handle errors appropriate to its level
- Subsystems handle domain-specific errors
- Hub layer handles integration and coordination errors
- Tool layer handles MCP-specific error formatting
- Use consistent error types and messages

**Documentation**:

- All public functions must have comprehensive docstrings
- Include parameter descriptions and return value documentation
- Provide usage examples for complex functions
- Document architectural decisions in code comments


Testing Strategy
------------------------------------------------------------------------------
**Unit Testing by Layer**:

- **Subsystem Tests**: Test individual package functionality with mock dependencies
- **Integration Tests**: Test hub coordination between subsystems and config  
- **Tool Tests**: Test MCP tool implementations with mock hub calls
- **End-to-End Tests**: Test complete request flow through all layers

**Test File Organization**:

- Mirror source code structure in `tests/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/tests>`_ directory
- Each source file has corresponding test file
- Use descriptive test names that indicate what is being tested

**Mocking Strategy**:

- Mock external dependencies (databases, APIs) at subsystem boundaries
- Use dependency injection where possible to facilitate testing
- Test error conditions and edge cases thoroughly

This architecture provides a solid foundation for building a maintainable, testable, and extensible MCP server while keeping concerns properly separated and dependencies minimal.
