.. _system-integration-guide:

System Integration Guide: Understanding the Complete Architecture
==============================================================================
*How all components work together to deliver MCP database capabilities*


Overview
------------------------------------------------------------------------------
This document brings together all the individual components covered in the :ref:`developer-guide` to explain how the ``mcp_ohmy_sql`` system works as a **unified whole**. Understanding this integration is essential for maintainers who need to add features, fix bugs, or extend the system to support new database types.

The ``mcp_ohmy_sql`` architecture follows a **layered, modular design** where each component has a specific responsibility, yet all components work together seamlessly to deliver database access through the Model Context Protocol (MCP).

**Architecture Summary**:

.. code-block:: text

    User Request → MCP Tools → Adapters → Configuration + Database Operations
                                     ↘                  ↙
                                      SDK Utilities + db/ Module
                                      (Per-Database)   (Schema Processing)


System Components Overview
------------------------------------------------------------------------------
Let's revisit how each component fits into the larger system:

**1. Database Metadata Module** (:ref:`Database Metadata Module <database-metadata-module>`)
    Foundation layer that extracts and processes database schemas using the three-layer Model-Encoder-Extractor pattern.

**2. Per-SDK Utilities** (:ref:`Per-SDK Utilities <per-sdk-utilities>`)
    Database-specific connection and query utilities that wrap external SDKs (SQLAlchemy, boto3, etc.).

**3. Configuration System** (:ref:`Configuration System <configuration-system>`)
    Hierarchical JSON-based configuration that defines databases, schemas, and access rules.

**4. Adapter System** (:ref:`Adapters <adapters>`)
    Integration bridge that combines configuration with database operations to create MCP tools.

**5. Real Database Testing** (:ref:`Real Database Testing Strategy <real-database-testing>`)
    Comprehensive testing strategy using actual databases to ensure reliability.


Complete Data Flow: From User Request to Database Response
------------------------------------------------------------------------------
Understanding how a typical request flows through the entire system helps clarify where to make changes for different types of modifications.

**Example: "Get schema details for database 'ecommerce'"**

.. code-block:: text

    1. MCP Client Request
       ↓
    2. MCP Server (tools.py)
       - Receives tool call: get_schema_details(database_id="ecommerce")
       - Forwards to adapter layer
       ↓
    3. Adapter Layer (adapter/tool_adapter.py)
       - Validates database_id exists in configuration
       - Retrieves Database configuration object
       - Determines database type (postgres, sqlite, aws_redshift, etc.)
       ↓
    4. Configuration Resolution (config/define.py)
       - Loads Database object with connection details
       - Gets Schema objects with filtering rules
       - Validates all configuration constraints
       ↓
    5. Database Connection (sdk utilities + db/ extractors)
       - SDK utility establishes connection (sa/, aws/, etc.)
       - db/ extractor queries database metadata
       - Three-layer processing: raw data → models → encoded output
       ↓
    6. Result Processing (adapter/tool_adapter.py)
       - Formats encoded schema as MCP tool response
       - Adds performance timing information
       - Returns structured JSON to MCP client


Where to Make Changes: Developer Decision Tree
------------------------------------------------------------------------------
When modifying the system, use this decision tree to identify which components need changes:

**Adding a New Database Type** (e.g., MongoDB support)
    1. Create new SDK utility module: ``mcp_ohmy_sql/mongodb/`` (:ref:`Per-SDK Utilities <per-sdk-utilities>`)
    2. Add database-specific subdirectory: ``mcp_ohmy_sql/db/mongodb/`` (:ref:`Database Metadata Module <database-metadata-module>`)
    3. Implement three-layer pattern: models, encoders, extractors (:ref:`Model-Encoder-Extractor <model-encoder-extractor>`)
    4. Add connection configuration: ``mcp_ohmy_sql/config/mongodb.py`` (:ref:`Configuration System <configuration-system>`)
    5. Update adapter logic: ``mcp_ohmy_sql/adapter/`` (:ref:`Adapters <adapters>`)
    6. Add test database provisioning (:ref:`Real Database Testing Strategy <real-database-testing>`)

**Adding a New MCP Tool** (e.g., execute_insert_statement)
    1. Add tool implementation: ``mcp_ohmy_sql/adapter/tool_adapter.py`` (:ref:`Adapters <adapters>`)
    2. Add MCP wrapper: ``mcp_ohmy_sql/tools.py``
    3. Update configuration if new settings needed (:ref:`Configuration System <configuration-system>`)
    4. Add integration tests (:ref:`Real Database Testing Strategy <real-database-testing>`)

**Modifying Schema Encoding** (e.g., change LLM format)
    1. Update encoder functions: ``mcp_ohmy_sql/db/*/schema_2_encoder.py`` (:ref:`Model-Encoder-Extractor <model-encoder-extractor>`)
    2. Update model definitions if needed: ``mcp_ohmy_sql/db/*/schema_1_model.py``
    3. Verify adapter layer compatibility: ``mcp_ohmy_sql/adapter/`` (:ref:`Adapters <adapters>`)
    4. Update relevant unit tests

**Adding Configuration Options** (e.g., query timeout settings)
    1. Update configuration models: ``mcp_ohmy_sql/config/define.py`` (:ref:`Configuration System <configuration-system>`)
    2. Update adapters to use new settings: ``mcp_ohmy_sql/adapter/`` (:ref:`Adapters <adapters>`)
    3. Update SDK utilities if connection behavior changes (:ref:`Per-SDK Utilities <per-sdk-utilities>`)
    4. Add configuration validation tests

**Performance Optimization** (e.g., caching, connection pooling)
    1. Identify bottleneck location using the data flow diagram above
    2. For connection issues: modify SDK utilities (:ref:`Per-SDK Utilities <per-sdk-utilities>`)
    3. For metadata extraction: optimize db/ extractors (:ref:`Database Metadata Module <database-metadata-module>`)
    4. For encoding: optimize encoders (:ref:`Model-Encoder-Extractor <model-encoder-extractor>`)
    5. Add performance test cases (:ref:`Real Database Testing Strategy <real-database-testing>`)

**Bug Fixes**
    1. Identify which layer contains the bug using error traces
    2. Write a failing test that reproduces the issue
    3. Fix the bug in the appropriate component
    4. Ensure fix doesn't break integration between components


Component Integration Patterns
------------------------------------------------------------------------------
**Configuration → Database Operations**
    The :class:`~mcp_ohmy_sql.config.define.Database` object contains all information needed to establish connections and perform operations. Adapters convert configuration objects into executable database calls.

    .. code-block:: python

        # Configuration drives database operations
        database_config = config.databases_mapping["my_db"]
        connection = database_config.connection.create_connection()
        schemas = extract_all_schemas(connection, database_config.schemas)

**SDK Utilities ↔ db/ Module**
    SDK utilities handle connection management and low-level operations, while the db/ module processes metadata. They work together but remain independent.

    .. code-block:: python

        # SDK utility provides connection, db/ module processes metadata
        engine = sqlalchemy_connection.sa_engine  # SDK utility
        extractor = RelationalExtractor()          # db/ module
        schema_info = extractor.extract_schema_info(engine, schema_config)

**Adapters as Integration Hub**
    Adapters orchestrate all other components without containing business logic themselves. They handle error cases and coordinate complex operations.

    .. code-block:: python

        # Adapter coordinates but delegates actual work
        def get_schema_details(database_id: str) -> dict:
            config = load_configuration()                    # Configuration
            db_config = config.databases_mapping[database_id]  # Configuration
            connection = create_connection(db_config)        # SDK Utility
            schema_info = extract_schemas(connection)        # db/ Module
            return format_response(schema_info)              # Adapter logic


Testing Integration Points
------------------------------------------------------------------------------
The :ref:`Real Database Testing Strategy <real-database-testing>` ensures all integration points work correctly with actual databases. Key integration tests verify:

**Configuration → Database Connection**
    Test that configuration objects successfully establish connections to real databases.

**Schema Extraction → Encoding**
    Test that extracted metadata is correctly encoded into AI-friendly formats.

**Adapter Coordination**
    Test that adapters correctly orchestrate all components for complete tool functionality.

**Cross-Database Consistency**
    Test that the same operations work consistently across different database types.


Error Handling Integration
------------------------------------------------------------------------------
Errors can occur at any integration point. The system handles errors systematically:

**Configuration Errors** (Invalid JSON, missing fields)
    Caught during configuration loading with detailed validation messages.

**Connection Errors** (Network issues, authentication failures)  
    Handled by SDK utilities with clear error messages for troubleshooting.

**Extraction Errors** (Permission issues, unsupported features)
    Managed by db/ extractors with graceful degradation when possible.

**Integration Errors** (Component version mismatches, API changes)
    Detected by adapters with context about which integration failed.


Extension Points for New Features
------------------------------------------------------------------------------
The modular architecture provides clear extension points:

**New Database Types**
    Add new subdirectories in both SDK utilities and db/ modules following existing patterns.

**New Data Sources** (Beyond databases)
    Create new top-level modules parallel to existing database modules.

**New Output Formats**
    Add new encoder functions in the db/ module's second layer.

**New MCP Tools**
    Add new adapter functions that combine existing components in new ways.

**New Configuration Options**
    Extend the configuration hierarchy while maintaining backward compatibility.


Best Practices for System Modifications
------------------------------------------------------------------------------

**1. Follow the Separation of Concerns**
    Each component should handle only its designated responsibility. Don't add database-specific logic to adapters or MCP-specific logic to the db/ module.

**2. Maintain Component Independence**  
    Components should communicate through well-defined interfaces. Avoid tight coupling between database-specific modules.

**3. Test Integration Points**
    When modifying any component, test its integration with adjacent components using real databases.

**4. Update Documentation**
    Changes to component interfaces or integration patterns should be reflected in the relevant Developer Guide sections.

**5. Preserve Configuration Compatibility**
    Changes should maintain backward compatibility with existing configuration files when possible.


Conclusion
------------------------------------------------------------------------------
The mcp_ohmy_sql system achieves its flexibility and maintainability through careful separation of concerns and well-defined integration patterns. Each component can be developed, tested, and maintained independently while contributing to a cohesive whole.

When working on the system:

- **Use the data flow diagram** to understand how your changes affect the request/response cycle
- **Follow the decision tree** to identify which components need modification
- **Test integration points** to ensure your changes don't break component coordination
- **Maintain the architectural patterns** that make the system predictable and extensible

This architecture enables the system to grow and adapt while maintaining reliability and ease of maintenance for future developers.

.. seealso::

    - :ref:`Database Metadata Module <database-metadata-module>` - Core schema processing
    - :ref:`Model-Encoder-Extractor <model-encoder-extractor>` - Three-layer architecture
    - :ref:`Per-SDK Utilities <per-sdk-utilities>` - Database-specific operations
    - :ref:`Configuration System <configuration-system>` - Hierarchical configuration
    - :ref:`Adapters <adapters>` - Integration bridge
    - :ref:`Real Database Testing Strategy <real-database-testing>` - Comprehensive testing