.. _database-metadata-module:

Database Metadata Module (db/)
==============================================================================
*Understanding the core database schema extraction functionality that powers the MCP server*


Overview
------------------------------------------------------------------------------
The `mcp_ohmy_sql/db/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/db>`_ module represents the foundational layer of this library - it contains the core logic for extracting database schema information and encoding it properly for AI consumption. This module is designed to be database-agnostic, supporting different database systems through specialized sub-modules.

The primary purpose of this module is to:

- Pull comprehensive database schema information from various database systems
- Extract table and column definition metadata  
- Transform raw database metadata into structured, AI-friendly formats
- Provide a consistent interface across different database technologies


Core Design Philosophy
------------------------------------------------------------------------------
The ``db/`` module follows a **bottom-up, database-specific approach**:

1. **Database Independence**: Each database system has its own sub-module with system-specific extraction logic
2. **Consistent Interface**: All sub-modules follow the same architectural pattern for predictable behavior
3. **Schema-First Design**: Focus on comprehensive metadata extraction rather than data querying
4. **AI Optimization**: Structure information in formats that work well with language models


Module Structure
------------------------------------------------------------------------------
.. code-block:: text

    mcp_ohmy_sql/db/
    ├── __init__.py              # Package initialization
    ├── metadata.py              # Common metadata utilities and base classes
    ├── relational/              # Generic relational database support
    ├── more_database_1/         # Database 1 specific implementation
    ├── more_database_2/         # Database 2 specific implementation
    └── ...


Database-Specific Sub-modules
------------------------------------------------------------------------------
Each database system is implemented as a separate sub-module following a consistent three-layer pattern:

**Layer 1: Models (schema_1_model.py)**
    Data structures that represent database schema elements (databases, schemas, tables, columns, etc.)

**Layer 2: Encoders (schema_2_encoder.py)**  
    Logic to transform raw database metadata into structured, AI-friendly formats

**Layer 3: Extractors (schema_3_extractor.py)**
    Implementation that connects to databases and pulls metadata using system-specific queries

.. code-block:: text

    mcp_ohmy_sql/db/relational/
    ├── __init__.py
    ├── api.py                # Public API for relational databases
    ├── schema_1_model.py     # Data models for schema representation
    ├── schema_2_encoder.py   # Schema encoding logic
    └── schema_3_extractor.py # Schema extraction implementation


Independence and Modularity
------------------------------------------------------------------------------
The ``db/`` module is designed to be **completely independent** from other parts of the system:

- No dependencies on configuration management
- No dependencies on MCP server functionality  
- No dependencies on integration layers
- Can be used standalone for database schema analysis

This independence makes the module:

- **Testable**: Easy to unit test without complex setup
- **Reusable**: Can be integrated into other projects
- **Maintainable**: Changes don't affect other system components
- **Extensible**: New database systems can be added without modifying existing code


Next Steps
------------------------------------------------------------------------------
This module serves as the foundation for the entire MCP server. The extracted schema information flows upward through:

1. **Adapter Layer**: Coordinates database operations and manages connections
2. **Integration Layer**: Combines schema information with configuration and business logic  
3. **Tool Layer**: Exposes schema information through MCP tools for AI consumption

Understanding this ``db/`` module is essential for contributors who want to:

- Add support for new database systems
- Modify schema extraction logic
- Optimize metadata encoding for AI consumption  
- Troubleshoot database connectivity issues
