# Code Structure Guide for mcp_ohmy_sql

This document provides a comprehensive guide to the codebase structure and architecture of the mcp_ohmy_sql project.

## Overview

mcp_ohmy_sql is a Model Context Protocol (MCP) server that provides SQL database capabilities through SQLAlchemy. The project follows a layered, modular architecture that promotes separation of concerns, testability, and maintainability.

## Core Design Philosophy

The mcp_ohmy_sql project is built around three fundamental principles:

1. **Separation of Concerns**: Each subsystem (SQLAlchemy, AWS, Elasticsearch, DuckDB, etc.) operates independently without cross-dependencies
2. **Integration Layer**: A central hub module provides controlled integration between subsystems and configuration
3. **Testability**: The architecture allows easy unit testing without requiring a full MCP server setup

## Project Structure

```
mcp_ohmy_sql/
├── __init__.py              # Package initialization
├── _version.py              # Version information
├── api.py                   # Public API exports
├── app.py                   # Main entry point for MCP server
├── config/                  # Configuration management system
│   ├── __init__.py
│   ├── api.py               # Config module public API
│   ├── config_define.py     # Core configuration classes and database definitions
│   └── config_init.py       # Configuration initialization and loading logic
├── constants.py             # Project constants and enums
├── create_app.py            # MCP server factory
├── docs/                    # Internal documentation
│   ├── __init__.py
│   └── mcp_instructions.md  # MCP server instructions
├── hub/                     # Integration layer
│   ├── __init__.py
│   ├── api.py               # Hub module public API
│   ├── hub.py               # Central hub coordinating configuration and subsystems
│   ├── hub_init.py          # Hub initialization logic
│   ├── sa_hub.py            # SQLAlchemy-specific integration logic
│   └── tool_hub.py          # MCP tool implementations
├── paths.py                 # Path utilities
├── server.py                # MCP server definition
├── tools.py                 # MCP tool wrapper layer
├── sa/                      # SQLAlchemy subsystem package
│   ├── __init__.py
│   ├── api.py               # SA module public API
│   ├── metadata.py          # Database schema introspection
│   ├── query.py             # Query execution functionality
│   ├── schema_encoder.py    # LLM-friendly schema encoding
│   └── types.py             # Type definitions and mappings
├── aws/                     # AWS subsystem package (future)
│   ├── __init__.py
│   └── api.py
├── tests/                   # Internal test helpers
├── utils.py                 # Utility functions
└── vendor/                  # Third-party dependencies
```

## Architectural Layers

The codebase is organized into distinct layers, each with specific responsibilities:

```
User Request → MCP Client → tools.py → hub/tool_hub → hub → subsystem packages → Database/Service
```

### Layer 1: Entry Point (config/)
**Purpose**: Configuration management and application bootstrapping

**Responsibilities**:
- Load and validate configuration from environment variables
- Parse JSON configuration files
- Provide configuration objects to other layers
- Manage database connection parameters
- Handle multi-database, multi-schema configurations

**Key Files**:
- `config_define.py`: Core configuration classes and database definitions
- `config_init.py`: Configuration loading and initialization logic

### Layer 2: Subsystem Packages
**Purpose**: Domain-specific tool implementations

**Locations**:
- `sa/` (SQLAlchemy tools)
- `aws/` (AWS tools - future)
- Additional subsystems can be added independently

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

### Layer 3: Integration Layer (hub/)
**Purpose**: Coordinate between configuration and subsystem packages

**Responsibilities**:
- Bridge configuration objects with subsystem implementations
- Manage cross-subsystem interactions
- Handle resource lifecycle (connections, sessions, etc.)
- Provide unified error handling and logging
- Coordinate complex operations that span multiple subsystems

**Key Files**:
- `hub.py`: Central hub class coordinating all subsystems
- `sa_hub.py`: SQLAlchemy-specific integration logic
- `tool_hub.py`: MCP tool implementations

**Design Benefits**:
- Subsystems remain decoupled from each other
- Configuration changes don't directly impact subsystem code
- Complex workflows can be orchestrated without tight coupling
- Easy to add new subsystems without modifying existing ones

### Layer 4: MCP Tool Implementation (hub/tool_hub.py)
**Purpose**: Low-level MCP tool implementations

**Responsibilities**:
- Implement MCP-specific tool logic
- Handle MCP protocol requirements (serialization, error formats, etc.)
- Coordinate calls to hub integration layer
- Manage tool-specific validation and error handling
- Provide tool metadata and documentation

**Current Tools**:
- `tool_list_databases()`: List all configured databases
- `tool_list_tables()`: List tables in a database schema
- `tool_get_database_details()`: Get complete schema information for all databases
- `tool_get_schema_details()`: Get detailed schema for a specific database
- `tool_execute_select_statement()`: Execute SELECT queries with performance timing

### Layer 5: MCP Tool Wrapper (tools.py)
**Purpose**: Thin wrapper exposing tools to MCP server

**Responsibilities**:
- Register MCP tools with FastMCP server
- Provide tool decorators and metadata
- Forward requests to tool_hub implementations
- Handle MCP server integration

**Design Benefits**:
- Minimal code in the MCP interface layer
- Easy to add/remove tools without complex changes
- Tool logic remains testable independently of MCP
- Clear separation of MCP concerns from business logic

## Configuration Schema

The project uses a JSON-based configuration system with the following structure:

```json
{
    "version": "0.1.1",
    "settings": {},
    "databases": [
        {
            "identifier": "unique_db_id",
            "description": "Database description",
            "db_type": "sqlite",
            "connection": {
                "type": "sqlalchemy",
                "create_engine_kwargs": {
                    "url": "sqlite:////path/to/database.sqlite"
                }
            },
            "schemas": [
                {
                    "name": "default",
                    "table_filter": {
                        "include": ["table1", "table2"],
                        "exclude": ["temp_*"]
                    }
                }
            ]
        }
    ]
}
```

## Data Flow Example

Here's how a typical request flows through the architecture:

1. **User Request**: "Get schema details for database 'chinook_sqlite'"
2. **MCP Layer** (`tools.py`): `get_schema_details()` receives the request and forwards to `tool_hub.tool_get_schema_details()`
3. **Tool Implementation** (`hub/tool_hub`): Validates the database identifier and calls hub integration layer
4. **Integration Layer** (`hub/`): Retrieves configuration for the specified database and initializes appropriate subsystem
5. **Subsystem Layer** (`sa/`): Connects to the database, performs schema introspection, and encodes schema information
6. **Response Path**: Results flow back through the same layers in reverse

## Current Capabilities

### Implemented
- Database schema introspection with full metadata
- Support for any SQLAlchemy-compatible database
- MCP protocol integration via FastMCP
- Configuration management system
- Query execution with performance timing
- Multi-database, multi-schema support

### Planned (Based on Project Goals)
- Data pagination to prevent large data loads to LLMs
- Data export to local files
- Access control features
- Configurable tool exposure (enable/disable specific tools)
- Query optimization and caching
- Additional subsystem support (AWS, Elasticsearch, DuckDB)

## Development Guidelines

### Adding New MCP Tools
1. Implement core functionality in appropriate subsystem package (`sa/`, `aws/`, etc.)
2. Add integration logic to `hub/` if needed
3. Implement tool in `hub/tool_hub.py` with proper error handling
4. Add wrapper function to `tools.py` with `@mcp.tool()` decorator
5. Write unit tests covering all layers

### Adding a New Subsystem
1. Create new package: `mcp_ohmy_sql/new_subsystem/`
2. Implement service-specific functionality following the `sa/` pattern
3. Add integration logic to `hub/` for coordinating with config
4. Implement MCP tools in `hub/tool_hub.py`
5. Add wrapper functions to `tools.py`
6. Update configuration schema to support new subsystem

### Configuration Changes
1. Update the configuration schema in `config/config_define.py`
2. Ensure backward compatibility with existing config files
3. Update documentation and examples

### Database Operations
1. All SQL operations should go through the appropriate subsystem package
2. Use SQLAlchemy's reflection and metadata capabilities
3. Implement proper error handling and connection management

## Installation Modes

The project is currently local-only but will support:
- **UV installable**: Modern Python package installer
- **Pip installable**: Traditional PyPI distribution
- **Docker installable**: Containerized deployment

## Virtual Environment Setup

We create the Python virtual environment in the `.venv` directory at the project root. Key tools include:

- `.venv/bin/python`: Virtual environment Python interpreter, used 99% of the time
- `.venv/bin/pip`: pip package manager for installing ad-hoc Python packages. For predefined packages in `pyproject.toml`, we primarily use the global `poetry` 2.x command
- `.venv/bin/pytest`: pytest test runner for executing unit tests

## Test Strategy

### Unit Test File Organization

Each Python file in `mcp_ohmy_sql/` has a corresponding unit test file in the `tests/` directory. For example, source code at `mcp_ohmy_sql/my_package/my_subpackage/my_module.py` has its test file at `tests/my_package/my_subpackage/test_my_package_my_subpackage_my_module.py`. The test file name includes the full relative path to prevent naming collisions.

### Package Test Directory Structure

Each Python package (directory containing `__init__.py`) has a corresponding test directory in `tests/`. For example, the package at `mcp_ohmy_sql/my_package/my_subpackage/` has its test directory at `tests/my_package/my_subpackage/`. Each test directory contains an `all.py` file that runs code coverage tests for all modules in that package.

### Running Code Coverage Tests for Individual Files

Each test file can be run directly to generate a coverage report:

```bash
.venv/bin/python tests/my_package/my_subpackage/test_my_package_my_subpackage_my_module.py
```

This will:

1. Run all unit tests for the specific module
2. Generate a code coverage HTML report at `htmlcov/${random_hash}_my_module_py.html`
3. Show covered and uncovered lines in the HTML report

This is the most important workflow since 90% of development involves editing a single source file and running its corresponding test to meet coverage goals.

### Running Code Coverage Tests for All Files

Each source code directory has a corresponding `all.py` test script. Running `tests/all.py` executes code coverage tests for the entire Python package:

```bash
.venv/bin/python tests/all.py
```

You can also run coverage tests for a specific package:

```bash
.venv/bin/python tests/my_package/all.py
```

### Code Coverage Configuration

The `.coveragerc` file in the root directory configures the coverage tool, specifying which files to exclude from coverage reports in the `omit` section.

### Viewing Coverage Reports

After running tests, open the generated HTML file to see:

- Green lines: Code executed during tests
- Red lines: Code not covered by tests  
- Line-by-line coverage details

### Coverage Goals

- Target 95%+ code coverage for all implementation files
- Use `# pragma: no cover` for untestable code (e.g., platform-specific code when testing on different platforms)

## Public API and Testing

The package always includes a `mcp_ohmy_sql/api.py` file that exposes all public APIs for package users. Each line in this file defines a Python class, function, or variable.

We follow this pattern:

```python
from .my_module import my_func_1
from .my_module import my_func_2
```

We avoid this pattern:

```python
from .my_module import my_func_1, my_func_2
```

The corresponding test file is located at `tests/test_api.py`. This test file imports all public API objects from `mcp_ohmy_sql/api.py` to establish a test baseline, ensuring that any changes to the public API in `api.py` are caught by unit tests.
