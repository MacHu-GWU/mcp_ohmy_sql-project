.. _per-sdk-utilities:

Per-SDK Utilities: Simplified Database Integration
==============================================================================
*Understanding the independent utility modules that wrap external database SDKs*


Overview
------------------------------------------------------------------------------
To interact with different database systems, this project relies on various external Python SDKs (Software Development Kits). Each SDK has its own API patterns, connection methods, and quirks. The per-SDK utility system provides a **standardized abstraction layer** that simplifies and harmonizes these different SDKs for consistent use throughout the project.

These utility modules are **completely independent** from the core database metadata extraction system (`db/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/db>`_ module) and serve as reusable components that could be used in other projects.

**Key Design Principles**:

- **SDK-Specific**: Each utility module focuses on one external SDK
- **Independence**: No dependencies on other project modules (except constants/utils)
- **Simplification**: Provide easier-to-use interfaces for common operations
- **Standardization**: Consistent patterns across different database technologies


Currently Supported SDKs
------------------------------------------------------------------------------
**SQLAlchemy** (`sa/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/sa>`_)
  Universal Python SQL toolkit for relational databases

**AWS Redshift** (`aws/aws_redshift/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/aws/aws_redshift>`_)
  Amazon Redshift data warehouse with boto3 and redshift-connector

**Future SDK Support**:
  - Elasticsearch
  - DuckDB
  - MongoDB
  - Snowflake


SDK Integration Pattern
------------------------------------------------------------------------------
Each SDK utility module follows a consistent organizational pattern:


**Standardized Structure**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: text

    mcp_ohmy_sql/{sdk_name}/
    ├── __init__.py          # Package initialization
    ├── api.py               # Public API - what other modules should import
    ├── {specific}.py        # SDK-specific functionality modules
    └── utils.py             # General utilities and helper functions


**Public API Pattern**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Every SDK module exposes its functionality through ``api.py``:

.. code-block:: python

    # mcp_ohmy_sql/sa/api.py
    from .utils import get_create_view_sql
    from .utils import get_drop_view_sql  
    from .query import execute_select_query

This pattern ensures:

- **Clear Interface**: Other modules only import from ``api.py``
- **Internal Flexibility**: Implementation can be reorganized without breaking consumers
- **Consistent Imports**: All SDK modules use the same import pattern


Usage in Database Module
------------------------------------------------------------------------------
The per-SDK utilities are consumed by the database metadata extraction system (``db/`` module) but remain independent:

**In Database Extractors**:

.. code-block:: python

    # In db/relational/schema_3_extractor.py
    from ...sa.api import execute_select_query  # For SQLAlchemy operations

**Benefits of This Architecture**:

- **Modularity**: SDK utilities can be developed and tested independently
- **Reusability**: Utilities can be used in other projects without the database extraction system
- **Maintainability**: Changes to SDK utilities don't affect database extraction logic
- **Testability**: Each layer can be tested with appropriate mocking strategies


Testing Strategy
------------------------------------------------------------------------------
Each SDK utility module has its own comprehensive test suite:


**Unit Testing Approach**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**SQLAlchemy Tests** (`tests/sa/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/tests/sa>`_)
  - Use in-memory SQLite databases for fast, isolated testing
  - Test SQL generation across different database dialects
  - Mock external dependencies where appropriate


**Test Organization**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Following the project's testing conventions:

- Each source file has a corresponding test file
- Tests run code coverage analysis
- Separate test directories mirror the source structure
- ``all.py`` files provide package-level test execution


Independence and Reusability
------------------------------------------------------------------------------
The per-SDK utility system is designed for maximum independence:

**No Project Dependencies**
  SDK utilities only depend on:
  - The specific external SDK they wrap
  - Project constants (database types, etc.)
  - Basic utility functions

**Self-Contained Functionality**  
  Each SDK module could be extracted and used in other projects without modification.

**Clean Interfaces**
  All functionality is exposed through well-documented public APIs.

**Consistent Patterns**
  New SDK modules can follow the established patterns for predictable integration.

This architecture enables the project to support multiple database technologies while keeping the integration layer clean and the utilities reusable across different contexts.