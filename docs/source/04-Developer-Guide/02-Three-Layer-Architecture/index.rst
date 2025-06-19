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

.. code-block:: python

    DatabaseInfo
    └── schemas: List[SchemaInfo]
        └── tables: List[TableInfo] 
            └── columns: List[ColumnInfo]
                └── foreign_keys: List[ForeignKeyInfo]

**Key Model Classes**:

**ForeignKeyInfo**
  Represents foreign key constraints with relationship metadata:

  .. code-block:: python

    class ForeignKeyInfo(BaseInfo):
        object_type: ObjectTypeEnum = Field(default=ObjectTypeEnum.FOREIGN_KEY)
        onupdate: Optional[str] = Field(default=None)      # CASCADE, SET NULL, etc.
        ondelete: Optional[str] = Field(default=None)      # CASCADE, RESTRICT, etc.
        deferrable: Optional[bool] = Field(default=None)    # Constraint checking timing
        initially: Optional[str] = Field(default=None)      # DEFERRED or IMMEDIATE

**ColumnInfo**
  Comprehensive column metadata with type information and constraints:

  .. code-block:: python

    class ColumnInfo(BaseColumnInfo):
        fullname: str = Field()                           # table.column format
        type: str = Field()                               # Raw database type
        llm_type: Optional[LLMTypeEnum] = Field()         # Simplified AI type
        primary_key: bool = Field(default=False)
        nullable: bool = Field(default=False)
        index: Optional[bool] = Field(default=None)
        unique: Optional[bool] = Field(default=None)
        constraints: List[str] = Field(default_factory=list)
        foreign_keys: List[ForeignKeyInfo] = Field(default_factory=list)

**TableInfo**
  Table-level metadata with column relationships:

  .. code-block:: python

    class TableInfo(BaseTableInfo):
        fullname: str = Field()                           # schema.table format
        primary_key: List[str] = Field()                  # Primary key column names
        foreign_keys: List[ForeignKeyInfo] = Field()     # Table-level foreign keys
        columns: List[ColumnInfo] = Field()               # All table columns

**Design Benefits**:

- **Type Safety**: Pydantic validation catches data inconsistencies early
- **Serialization**: Easy conversion to/from JSON for testing and debugging
- **Documentation**: Field definitions serve as living documentation
- **Extensibility**: New fields can be added without breaking existing code


Layer 2: Schema Encoders (schema_2_encoder.py)
------------------------------------------------------------------------------
**Purpose**: Transform structured model objects into compact, AI-optimized text representations

**Location**: ``mcp_ohmy_sql/db/relational/schema_2_encoder.py``

**Core Responsibility**: 
Convert verbose database metadata into token-efficient formats that preserve essential information while reducing LLM context usage by ~70%.

Encoding Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The encoder uses a **hierarchical, constraint-aware approach** that prioritizes:

1. **Token Efficiency**: Minimize text length while preserving semantics
2. **Semantic Clarity**: Use intuitive abbreviations (PK, FK, NN)
3. **Relationship Visibility**: Show foreign key relationships inline
4. **Constraint Logic**: Avoid redundant constraint information

Column Encoding Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Columns are encoded in a compact format that preserves all essential metadata:

**Format**: ``${COLUMN_NAME}:${DATA_TYPE}${CONSTRAINTS}``

**Constraint Abbreviations**:

- ``*PK``: Primary Key (implies unique and indexed)
- ``*UQ``: Unique constraint (implies indexed)  
- ``*NN``: Not Null constraint
- ``*IDX``: Has database index
- ``*FK->Table.Column``: Foreign key reference

**Smart Constraint Logic**:

.. code-block:: python

    # If column is primary key, omit redundant not-null constraint
    if pk:
        nn = ""
    # If column is primary key or unique, omit redundant index constraint  
    if pk or uq:
        idx = ""

**Example Encodings**:

.. code-block:: text

    UserId:INT*PK                              # Primary key
    Email:STR*UQ*NN                           # Unique, not null  
    CategoryId:INT*NN*IDX*FK->Category.CategoryId  # Foreign key with index
    Description:STR                           # Simple nullable column

Table Encoding Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tables are encoded in a SQL-like format that's immediately recognizable:

.. code-block:: text

    Table Product(
        ProductId:INT*PK,
        ProductName:STR*NN,
        CategoryId:INT*NN*FK->Category.CategoryId,
        Price:DEC*NN,
        Stock:INT*NN,
        CreatedAt:TS*NN,
        UpdatedAt:TS
    )

**Benefits for AI Consumption**:

- **Visual Structure**: Mimics familiar SQL CREATE TABLE syntax
- **Compact Representation**: ~70% reduction in token usage
- **Self-Documenting**: Constraint annotations are intuitive
- **Relationship Clarity**: Foreign keys show target tables inline

Schema and Database Encoding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Higher-level structures maintain the hierarchical pattern:

.. code-block:: text

    Schema ecommerce(
        Table Customer(
            CustomerId:INT*PK,
            Email:STR*UQ*NN,
            FirstName:STR*NN
        ),
        Table Order(
            OrderId:INT*PK,
            CustomerId:INT*NN*FK->Customer.CustomerId,
            OrderDate:DT*NN
        )
    )

Layer 3: Schema Extractors (schema_3_extractor.py)
------------------------------------------------------------------------------

**Purpose**: Connect to databases and extract raw metadata using database-specific logic

**Location**: ``mcp_ohmy_sql/db/relational/schema_3_extractor.py``

**Core Responsibility**: 
Handle the complexity of database introspection, type mapping, and metadata extraction while providing a clean interface to higher layers.

Type Mapping System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The extractor includes a comprehensive mapping system that converts database-specific types to simplified LLM types:

.. code-block:: python

    SQLALCHEMY_TYPE_MAPPING = {
        # String types
        sa.String.__visit_name__: LLMTypeEnum.STR,
        sa.Text.__visit_name__: LLMTypeEnum.STR,
        sa.VARCHAR.__visit_name__: LLMTypeEnum.STR,
        
        # Numeric types  
        sa.Integer.__visit_name__: LLMTypeEnum.INT,
        sa.BigInteger.__visit_name__: LLMTypeEnum.INT,
        sa.Numeric.__visit_name__: LLMTypeEnum.DEC,
        sa.Float.__visit_name__: LLMTypeEnum.FLOAT,
        
        # Date/time types
        sa.DateTime.__visit_name__: LLMTypeEnum.DT,
        sa.TIMESTAMP.__visit_name__: LLMTypeEnum.TS,
        sa.Date.__visit_name__: LLMTypeEnum.DATE,
        
        # Special types
        sa.JSON.__visit_name__: LLMTypeEnum.STR,
        sa.UUID.__visit_name__: LLMTypeEnum.STR,
        sa.Boolean.__visit_name__: LLMTypeEnum.BOOL,
    }

**Benefits of Type Simplification**:

- **Consistency**: All databases use same simplified type names
- **AI Comprehension**: Reduced type variety improves LLM understanding
- **Token Efficiency**: Short type names reduce context usage

Metadata Extraction Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The extractor follows a systematic pipeline to build complete schema information:

**1. Connection and Inspection**:

.. code-block:: python

    def new_schema_info(engine, metadata, schema_name=None, include=None, exclude=None):
        insp = sa.inspect(engine)
        view_names = set(insp.get_view_names(schema=schema_name))
        materialized_view_names = set(insp.get_materialized_view_names())

**2. Object Type Detection**:

.. code-block:: python

    if table_name in view_names:
        object_type = ObjectTypeEnum.VIEW
    elif table_name in materialized_view_names:
        object_type = ObjectTypeEnum.MATERIALIZED_VIEW
    else:
        object_type = ObjectTypeEnum.TABLE

**3. Hierarchical Construction**:

The extractor builds objects from bottom-up:

- ``new_foreign_key_info()``: Extract foreign key constraints
- ``new_column_info()``: Build column metadata with foreign keys
- ``new_table_info()``: Assemble table with columns and relationships
- ``new_schema_info()``: Coordinate schema with table filtering
- ``new_database_info()``: Top-level database container

**Filtering and Selection**:

The extractor supports flexible table filtering:

.. code-block:: python

    # Include/exclude patterns using utility matching
    if match(table_name, include, exclude) is False:
        continue

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