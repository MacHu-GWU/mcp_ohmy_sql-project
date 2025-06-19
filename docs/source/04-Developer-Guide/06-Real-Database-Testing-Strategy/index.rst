.. _real-database-testing:

Real Database Testing Strategy
==============================================================================
*Comprehensive testing approach using actual database systems and infrastructure*


Overview
------------------------------------------------------------------------------
Testing database functionality requires **real database systems** rather than mocks or simulators. The ``mcp_ohmy_sql`` project implements a sophisticated testing strategy that provisions and manages actual database instances across multiple technologies, ensuring comprehensive validation of database operations, schema extraction, and query execution.

The testing strategy balances **realism with practicality** by using different approaches for different database types:

- **SQLite**: Local files for fast, isolated testing
- **PostgreSQL**: Docker containers for realistic SQL engine testing  
- **AWS Redshift**: Real cloud infrastructure for production-like validation

**Key Principles**:

- **Real Databases**: Use actual database systems, not mocks
- **Automated Provisioning**: Scripted setup and teardown of test environments
- **Reusable Fixtures**: pytest fixtures that manage database lifecycle
- **Sample Data**: Consistent Chinook dataset across all database types
- **Infrastructure as Code**: CDK for cloud resource provisioning

Test Infrastructure Architecture
------------------------------------------------------------------------------
The testing system follows a **layered fixture approach** that coordinates database provisioning, data loading, and test execution:

.. code-block:: text

    Test Execution
    ├── pytest Fixtures (conftest.py)
    │   ├── Database Provisioning
    │   ├── Schema Setup  
    │   └── Data Loading
    ├── Sample Data System (chinook/)
    │   ├── Data Models (SQLAlchemy ORM)
    │   ├── Data Loader (JSON to DataFrame)
    │   └── Data Files (Chinook dataset)
    ├── Database Setup Scripts
    │   ├── setup_relational_database.py
    │   └── setup_aws_redshift_database.py
    └── Infrastructure (aws/stacks/)
        └── CDK Stack for AWS Resources


Reusable Fixture System: conftest.py
------------------------------------------------------------------------------
**Purpose**: Centralized pytest fixture management for database testing

**Location**: `mcp_ohmy_sql/tests/conftest.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/tests/conftest.py>`_

The conftest.py file implements a **sophisticated fixture hierarchy** that manages the complete lifecycle of test databases:

**Data Container Classes**:

.. code-block:: python

    @dataclasses.dataclass
    class SaEngineObjs:
        engine: sa.Engine
        metadata: sa.MetaData
        db_type: DbTypeEnum

These dataclasses provide **structured access** to database objects and metadata, enabling consistent testing patterns across different database types.

**Fixture Categories**:

**In-Memory SQLite Fixtures**
  Fast, isolated fixtures for unit testing that create fresh SQLite databases for each test function.

**Real Database Factories**  
  Sophisticated factory fixtures that provision and configure actual database instances with proper cleanup.

**Configuration and Adapter Fixtures**
  Class-scoped fixtures that provide configured adapter instances for integration testing.

**AWS Redshift Fixtures**
  Cloud-based fixtures that manage real Redshift Serverless instances for production-like testing.

**Key Fixture Patterns**:

.. code-block:: python

    @pytest.fixture(scope="function")
    def in_memory_sqlite_engine_objs():
        # Create fresh SQLite database for each test
        engine = sa.create_engine("sqlite:///:memory:")
        create_all_tables(engine=engine, metadata=Base.metadata, drop_first=False)
        create_all_views(engine=engine, db_type=DbTypeEnum.SQLITE)
        
        # Yield database for testing
        yield SaEngineObjs(engine=engine, metadata=metadata, db_type=DbTypeEnum.SQLITE)
        
        # Cleanup after test
        drop_all_views(engine=engine, db_type=DbTypeEnum.SQLITE)
        drop_all_tables(engine=engine, metadata=Base.metadata)


Sample Data System: chinook/
------------------------------------------------------------------------------
**Purpose**: Provide consistent test data across all database systems

**Location**: `mcp_ohmy_sql/tests/chinook/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/tests/chinook>`_

The Chinook sample dataset provides a **realistic music store database** that includes:

- **Multiple tables** with foreign key relationships
- **Sample views** for testing complex queries
- **Varied data types** (strings, integers, decimals, dates)
- **Realistic data volume** for performance testing

**ChinookDataLoader**: :class:`~mcp_ohmy_sql.tests.chinook.chinook_data_loader.ChinookDataLoader`

The data loader implements a **sophisticated JSON-to-DataFrame pipeline**:

.. code-block:: python

    class ChinookDataLoader:
        @cached_property
        def data(self) -> dict:
            return json.loads(path_ChinookData_json.read_text(encoding="utf-8"))
        
        def get_table_df(self, table_name: str) -> pl.DataFrame:
            # Load raw JSON data
            df = pl.DataFrame(self.data[table_name])
            
            # Apply database-specific type conversions
            for col_name, col in table.columns.items():
                if isinstance(col.type, sa.Integer):
                    df = df.with_columns(pl.col(col_name).cast(pl.Int32))
                elif isinstance(col.type, sa.DateTime):
                    df = df.with_columns(pl.col(col_name).str.strptime(...))

**Benefits**:

- **Type Safety**: Automatic conversion between JSON and database types
- **Performance**: Polars DataFrames for efficient data processing
- **Consistency**: Same data across SQLite, PostgreSQL, and Redshift
- **Flexibility**: Easy to add new tables or modify existing data


Relational Database Setup: setup_relational_database.py
------------------------------------------------------------------------------
**Purpose**: Automated setup for SQLAlchemy-compatible databases

**Location**: `mcp_ohmy_sql/tests/setup_relational_database.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/tests/setup_relational_database.py>`_

**Key Functions**: :func:`~mcp_ohmy_sql.tests.setup_relational_database.create_all_tables`, :func:`~mcp_ohmy_sql.tests.setup_relational_database.create_all_views`, :func:`~mcp_ohmy_sql.tests.setup_relational_database.insert_all_data`

The relational setup script provides **idempotent database provisioning**:

**Schema Management**:

.. code-block:: python

    def create_all_tables(engine: sa.Engine, metadata: sa.MetaData, drop_first: bool = True):
        if drop_first:
            drop_all_tables(engine=engine, metadata=metadata)
        metadata.create_all(engine, checkfirst=True)

**View Creation**:
Uses the per-SDK utilities to generate database-specific CREATE VIEW statements, handling SQL dialect differences across database systems.

**Data Population**:
Leverages the ChinookDataLoader to populate tables with consistent sample data across different database types.

**Benefits**:

- **Database Agnostic**: Works with SQLite, PostgreSQL, MySQL, etc.
- **Idempotent**: Safe to run multiple times
- **Complete**: Tables, views, and data in single operation
- **Fast**: Optimized for test execution speed


AWS Redshift Setup: setup_aws_redshift_database.py
------------------------------------------------------------------------------
**Purpose**: Specialized setup for AWS Redshift cloud data warehouse

**Location**: `mcp_ohmy_sql/tests/setup_aws_redshift_database.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/tests/setup_aws_redshift_database.py>`_

**Key Functions**: :func:`~mcp_ohmy_sql.tests.setup_aws_redshift_database.create_all_redshift_tables`, :func:`~mcp_ohmy_sql.tests.setup_aws_redshift_database.insert_all_data_to_redshift`

AWS Redshift requires **specialized handling** due to its cloud-native architecture:

**Table Creation**:
Uses Redshift-specific SQL DDL statements optimized for columnar storage and distributed architecture.

**Data Loading Strategy**:

.. code-block:: python

    def insert_all_data_to_redshift(conn_or_engine: T_CONN_OR_ENGINE):
        for table in Base.metadata.sorted_tables:
            insert_data_to_one_table(conn_or_engine=conn_or_engine, table=table)

**Dual Loading Methods**:

1. **Direct INSERT**: Fast for small datasets using parameterized queries
2. **S3 COPY**: Scalable for large datasets using S3 staging and COPY commands

**Cloud Integration**:
- **S3 Staging**: Uses S3 for efficient bulk data loading
- **IAM Roles**: Proper authentication between Redshift and S3
- **Parquet Format**: Optimized data format for Redshift ingestion

**Benefits**:

- **Production-Like**: Tests against real Redshift infrastructure
- **Performance**: Optimized loading strategies for different data sizes
- **Security**: Proper IAM role-based authentication
- **Scalability**: Handles both small test datasets and larger validation data


Configuration-Driven Testing: test_adapter.py
------------------------------------------------------------------------------
**Purpose**: Demonstrate real-world adapter usage with actual databases

**Location**: `mcp_ohmy_sql/tests/test_adapter.py <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/mcp_ohmy_sql/tests/test_adapter.py>`_

The test adapter module shows how the **complete system integrates**:

.. code-block:: python

    from .test_config import DatabaseEnum, test_config
    test_adapter = Adapter(config=test_config)
    
    # Provision SQLite database
    sqlite_database = DatabaseEnum.chinook_sqlite
    setup_relational_database(
        engine=sqlite_database.connection.sa_engine,
        metadata=Base.metadata,
        db_type=sqlite_database.db_type_enum,
    )

**Integration Benefits**:

- **Real Configuration**: Uses actual configuration objects from test_config.py
- **Multiple Databases**: Can test across SQLite, PostgreSQL, and Redshift simultaneously
- **Adapter Testing**: Validates the complete configuration → adapter → database pipeline
- **Production Simulation**: Tests the exact same code paths used in production


Infrastructure as Code: aws/stacks/
------------------------------------------------------------------------------
**Purpose**: Provision real AWS infrastructure for Redshift testing

**Location**: `mcp_ohmy_sql/tests/aws/stacks/mcp_ohmy_sql_stack/ <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/tree/main/mcp_ohmy_sql/tests/aws/stacks/mcp_ohmy_sql_stack>`_

**CDK Infrastructure**: :class:`~mcp_ohmy_sql.tests.aws.stacks.mcp_ohmy_sql_stack.iac_define.Stack`

The CDK stack provisions **complete AWS infrastructure** for testing:

**Infrastructure Components**:

.. code-block:: python

    def create_workgroup(self):
        self.workgroup = redshiftserverless.CfnWorkgroup(
            workgroup_name=self.workgroup_name,
            namespace_name=self.namespace_name,
            base_capacity=8,  # minimal capacity 8 RPUs
            publicly_accessible=True,
            subnet_ids=subnet_ids,
            security_group_ids=[self.sg.security_group_id],
        )

**Security Configuration**:
- **VPC Integration**: Uses existing VPC with proper subnet configuration
- **Security Groups**: Restricts access to developer IP addresses
- **IAM Roles**: Proper permissions for Redshift to access S3

**Cost Optimization**:
- **Serverless**: Pay-per-use pricing model
- **Minimal Capacity**: 8 RPU minimum for cost control
- **Automatic Cleanup**: CDK removal policies for resource cleanup

**Benefits**:

- **Reproducible**: Infrastructure defined as code
- **Secure**: Proper network and IAM security
- **Cost-Effective**: Minimal resource usage for testing
- **Realistic**: Production-like infrastructure for validation


Testing Workflow Integration
------------------------------------------------------------------------------
The complete testing workflow demonstrates how all components work together:

**Local Development**:
1. Run unit tests with in-memory SQLite fixtures
2. Validate against local PostgreSQL container
3. Execute integration tests with real AWS Redshift

**CI/CD Pipeline**:
1. Provision AWS infrastructure using CDK
2. Run test suite against all database types
3. Clean up infrastructure after testing

**Test Categories**:

**Unit Tests**
  Fast tests using in-memory SQLite with fixture-managed lifecycle

**Integration Tests**  
  Medium-speed tests using containerized PostgreSQL for realistic SQL engine behavior

**End-to-End Tests**
  Comprehensive tests using real AWS Redshift for production validation

**Performance Tests**
  Load testing using the full Chinook dataset across all database types


Architecture Benefits
------------------------------------------------------------------------------
**For Development**:

- **Fast Feedback**: In-memory SQLite for rapid unit testing
- **Realistic Testing**: Actual database engines catch real-world issues
- **Multi-Database**: Validates compatibility across different systems
- **Automated Setup**: No manual database configuration required

**For Quality Assurance**:

- **Production Parity**: Tests against same infrastructure as production
- **Comprehensive Coverage**: All database types and operations tested
- **Performance Validation**: Real query performance measurement
- **Security Testing**: Actual authentication and authorization mechanisms

**For Operations**:

- **Infrastructure Validation**: CDK ensures consistent environment provisioning
- **Cost Control**: Automated cleanup prevents resource waste
- **Monitoring**: Real AWS metrics and logging
- **Scalability Testing**: Validate performance under realistic loads

The real database testing strategy ensures that the MCP server works reliably across diverse database environments while maintaining development velocity through intelligent use of different testing approaches for different scenarios.
