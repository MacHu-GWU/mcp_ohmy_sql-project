.. _model-encoder-extractor:

Three-Layer Architecture: Model-Encoder-Extractor
==============================================================================
*Understanding the systematic approach to database schema processing in the db/ module*


Overview
------------------------------------------------------------------------------
Every database system in the `mcp_ohmy_sql/db/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/db>`_ module follows a standardized three-layer architecture that separates concerns and ensures consistent behavior across different database technologies. This document explains each layer using the `relational/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/db/relational>`_ sub-module as a concrete example.

The three layers work together in a pipeline:

- **Layer 1 - Model**: Structures the raw data into typed Python objects
- **Layer 2 - Encoder**: Transforms structured data into AI-friendly formats
- **Layer 3 - Extractor**: Connects to databases and extracts raw metadata


Architecture Flow
------------------------------------------------------------------------------
.. code-block:: text

    Database → Extractor → Model Objects → Encoder → AI-Friendly Text
    
    Raw SQL  → Layer 3   → Layer 1       → Layer 2 → Compact Schema
    Metadata               (Pydantic)              → Representation

This separation ensures that:

- Database-specific logic is isolated in extractors
- Data validation and structure is handled by models
- AI optimization is managed by encoders
- Each layer can be tested and modified independently


Layer 1: Data Models (schema_1_model.py)
------------------------------------------------------------------------------
**Purpose**: Define structured data containers for database schema elements

**Location**: `mcp_ohmy_sql/db/relational/schema_1_model.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/db/relational/schema_1_model.py>`_

**Core Responsibility**: Transform raw database metadata into strongly-typed Python objects using Pydantic for validation and serialization.


Hierarchical Model Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The models follow a hierarchical structure that mirrors database organization:

.. code-block:: text

    DatabaseInfo
    └── schemas: List[SchemaInfo]
        └── tables: List[TableInfo] 
            └── columns: List[ColumnInfo]
                └── foreign_keys: List[ForeignKeyInfo]

**Key Model Classes**: :class:`~mcp_ohmy_sql.db.relational.schema_1_model.ForeignKeyInfo`, :class:`~mcp_ohmy_sql.db.relational.schema_1_model.ColumnInfo`, :class:`~mcp_ohmy_sql.db.relational.schema_1_model.TableInfo`, :class:`~mcp_ohmy_sql.db.relational.schema_1_model.SchemaInfo`, :class:`~mcp_ohmy_sql.db.relational.schema_1_model.DatabaseInfo`

Each class uses Pydantic for type validation and serialization, ensuring data consistency and providing clear documentation through field definitions. The hierarchical structure enables easy navigation of database metadata while maintaining type safety throughout the system.

**Testing**: The model layer has minimal testing requirements since it primarily defines data structures. The corresponding test file `tests/db/relational/test_db_relational_schema_1_model.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/tests/db/relational/test_db_relational_schema_1_model.py>`_ contains simple import tests to ensure all model classes are properly defined and accessible.


Layer 2: Schema Encoders (schema_2_encoder.py)
------------------------------------------------------------------------------
**Purpose**: Transform structured model objects into compact, AI-optimized text representations

**Location**: `mcp_ohmy_sql/db/relational/schema_2_encoder.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/db/relational/schema_2_encoder.py>`_

**Core Responsibility**: Convert verbose database metadata into token-efficient formats that preserve essential information while reducing LLM context usage by ~70%.


Key Encoding Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The encoder provides specialized functions for each model type: :func:`~mcp_ohmy_sql.db.relational.schema_2_encoder.encode_column_info`, :func:`~mcp_ohmy_sql.db.relational.schema_2_encoder.encode_table_info`, :func:`~mcp_ohmy_sql.db.relational.schema_2_encoder.encode_schema_info`, :func:`~mcp_ohmy_sql.db.relational.schema_2_encoder.encode_database_info`

The encoding strategy focuses on **constraint-aware compression** - retaining maximum information while minimizing tokens through intelligent abbreviations and smart constraint logic that avoids redundant information (e.g., primary keys don't need explicit NOT NULL markers).

**Column Format**: ``${COLUMN_NAME}:${DATA_TYPE}${CONSTRAINTS}`` with abbreviations like ``*PK`` (Primary Key), ``*FK->Table.Column`` (Foreign Key), ``*NN`` (Not Null)

**Table Format**: SQL-like structure that's immediately recognizable to both humans and AI systems, preserving visual hierarchy while dramatically reducing token count.

**Testing**: The encoder layer requires comprehensive testing to ensure accurate schema representation. The test file `tests/db/relational/test_db_relational_schema_2_encoder.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/tests/db/relational/test_db_relational_schema_2_encoder.py>`_ creates mock schema model objects (ColumnInfo, TableInfo) with various constraint combinations and verifies the encoded output matches expected formats. Testing focuses on column and table encoding since schema and database objects are primarily data containers.


Layer 3: Schema Extractors (schema_3_extractor.py)
------------------------------------------------------------------------------
**Purpose**: Connect to databases and extract raw metadata using database-specific logic

**Location**: `mcp_ohmy_sql/db/relational/schema_3_extractor.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/db/relational/schema_3_extractor.py>`_

**Core Responsibility**: Handle the complexity of database introspection, type mapping, and metadata extraction while providing a clean interface to higher layers.

Key Extraction Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The extractor provides hierarchical construction functions: :func:`~mcp_ohmy_sql.db.relational.schema_3_extractor.new_foreign_key_info`, :func:`~mcp_ohmy_sql.db.relational.schema_3_extractor.new_column_info`, :func:`~mcp_ohmy_sql.db.relational.schema_3_extractor.new_table_info`, :func:`~mcp_ohmy_sql.db.relational.schema_3_extractor.new_schema_info`, :func:`~mcp_ohmy_sql.db.relational.schema_3_extractor.new_database_info`

The extraction mechanism leverages **SQLAlchemy's built-in introspection capabilities** to query system tables and metadata. For relational databases, this means using ``sa.inspect()`` and ``sa.MetaData.reflect()`` to discover tables, columns, constraints, and relationships. The key innovation is the comprehensive type mapping system that normalizes database-specific types into simplified LLM-friendly categories.

**Type Mapping**: Database-specific types (VARCHAR, BIGINT, TIMESTAMP) are mapped to universal categories (STR, INT, TS) for consistent AI consumption across different database systems.

**Object Construction**: Bottom-up approach building from foreign keys → columns → tables → schemas → databases, ensuring all relationships are properly captured.

**Testing**: The extractor layer requires real database connections for proper testing. The test file `tests/db/relational/test_db_relational_schema_3_extractor.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/tests/db/relational/test_db_relational_schema_3_extractor.py>`_ uses in-memory SQLite databases to test the complete extraction pipeline, verifying that SQLAlchemy objects are correctly transformed into the corresponding model objects with accurate metadata, types, and constraints.


Layer Integration Example
------------------------------------------------------------------------------
Here's how the three layers work together to process a database table:

**1. Raw Database Metadata** (what extractor receives):

.. code-block:: sql

    CREATE TABLE customer (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email VARCHAR(255) UNIQUE NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

**2. Model Objects** (after Layer 3 → Layer 1):

.. code-block:: python

    TableInfo(
        name="customer",
        object_type=ObjectTypeEnum.TABLE,
        columns=[
            ColumnInfo(
                name="customer_id",
                type="INTEGER",
                llm_type=LLMTypeEnum.INT,
                primary_key=True,
                nullable=False
            ),
            ColumnInfo(
                name="email", 
                type="VARCHAR(255)",
                llm_type=LLMTypeEnum.STR,
                unique=True,
                nullable=False
            )
        ]
    )

**3. AI-Friendly Output** (after Layer 1 → Layer 2):

.. code-block:: text

    Table customer(
        customer_id:INT*PK,
        email:STR*UQ*NN,  
        first_name:STR*NN,
        created_at:TS
    )


Architecture Benefits
------------------------------------------------------------------------------
**For Development**:

- **Clear Separation**: Each layer has distinct, well-defined responsibilities
- **Independent Testing**: Layers can be unit tested with mock dependencies
- **Predictable Patterns**: New database systems follow the same structure
- **Debugging Support**: Intermediate objects can be inspected and validated

**For Maintenance**:

- **Isolated Changes**: Modifications to one layer don't affect others
- **Type Safety**: Pydantic models catch data inconsistencies early
- **Documentation**: Code structure serves as architectural documentation
- **Extensibility**: New features can be added layer by layer

**For AI Integration**:

- **Optimized Output**: Encoders are specifically designed for LLM consumption
- **Consistent Format**: All database systems produce identical output format  
- **Token Efficiency**: Significant reduction in context usage
- **Semantic Preservation**: Essential schema information is retained despite compression
