# Code Structure Guide for mcp_ohmy_sql

This document provides a comprehensive guide to the codebase structure and architecture of the mcp_ohmy_sql project.

## Overview

mcp_ohmy_sql is a Model Context Protocol (MCP) server that provides SQL database capabilities through SQLAlchemy. The project follows a modular architecture with clear separation of concerns between database operations, MCP tool definitions, and server configuration.

## Project Structure

```
mcp_ohmy_sql/
├── __init__.py              # Package initialization
├── _version.py              # Version information
├── api.py                   # Public API exports
├── config/                  # Modular configuration system
│   ├── __init__.py
│   ├── config_define_00_main.py      # Main configuration definitions
│   ├── config_define_01_database_schema.py  # Database schema configuration
│   └── config_init.py       # Configuration initialization logic
├── constants.py             # Project constants and enums
├── create_app.py            # MCP server factory
├── docs/                    # Internal documentation
│   ├── __init__.py
│   └── mcp_instructions.md  # MCP server instructions
├── paths.py                 # Path utilities
├── server.py                # MCP server definition
├── tools.py                 # MCP tool implementations (wrapper layer)
├── sa/                      # SQLAlchemy core implementation
│   ├── __init__.py
│   ├── api.py               # SA module public API
│   ├── metadata.py          # Database schema introspection
│   ├── query.py             # Query execution functionality
│   ├── schema_encoder.py    # LLM-friendly schema encoding
│   └── types.py             # Type definitions and mappings
├── tests/                   # Internal test helpers
├── utils.py                 # Utility functions
└── vendor/                  # Third-party dependencies
```
## Architecture Flow

### 1. Entry Point (`app.py`)
- Main entry point for the MCP server
- Calls `create_app()` to get the configured server instance
- Runs the server with stdio transport for MCP communication

### 2. Application Factory (`create_app.py`)
- Factory method pattern for creating the MCP server
- Imports and registers all MCP tools from `tools.py`
- Returns the configured FastMCP server instance

### 3. MCP Server (`server.py`)
- Defines the FastMCP server instance using `FastMCP()`
- Loads instructions from `docs/mcp_instructions.md`
- Entry point for all MCP tool registrations

### 4. Configuration System (`config/` module)
- **Modular Design**: Configuration split into numbered modules for organization
  - `config_define_00_main.py`: Core configuration classes and database definitions
  - `config_define_01_database_schema.py`: Schema-related configuration methods
  - `config_init.py`: Configuration initialization and loading logic
- **Multi-Database Support**: Configuration supports multiple databases with multiple schemas each
- **Environment-driven**: Loads from `MCP_OHMY_SQL_CONFIG` environment variable
- **Configuration schema**:
  ```json
  {
      "version": "0.1.1",
      "settings": {},
      "databases": [
          {
              "identifier": "unique_db_id",
              "description": "Database description",
              "connection": {
                  "type": "sqlalchemy",
                  "create_engine_kwargs": {
                      "url": "sqlite:////path/to/database.sqlite"
                  }
              },
              "schemas": [
                  {
                      "name": "default",
                      // Optional, defaults to database default schema
                      "table_filter": {
                          "include": [
                              "table1",
                              "table2"
                          ],
                          // Optional whitelist
                          "exclude": [
                              "temp_*"
                          ]
                          // Optional blacklist
                      }
                  }
              ]
          }
      ]
  }
  ```

### 5. MCP Tools Layer (`tools.py`)
- **Purpose**: Wrapper layer that converts SQLAlchemy operations into MCP tools
- **Current Tools**: 
  - `get_database_schema()`: Get LLM-friendly schema representation
  - Additional tools to be implemented for query execution, data export, etc.
- **Design Pattern**: Each function decorated with `@mcp.tool()` becomes an available MCP tool
- **Data Flow**: tools.py → config/ → sa/ module → SQLAlchemy → Database

### 6. SQLAlchemy Core (`sa/` module)
- **Purpose**: Core SQL implementation providing database capabilities
- **Module Structure**:
  - `sa/api.py`: Public API exports for the SA module
  - `sa/metadata.py`: Database schema introspection
    - Pydantic models: `ForeignKeyInfo`, `ColumnInfo`, `TableInfo`, `SchemaInfo`
    - Support for tables, views, and materialized views
  - `sa/query.py`: Query execution and result handling
  - `sa/schema_encoder.py`: LLM-optimized schema encoding
    - Converts verbose metadata to compact format
    - ~70% token reduction for LLM consumption
  - `sa/types.py`: SQLAlchemy to LLM type mappings
    - Maps database types to simplified categories (STR, INT, DEC, etc.)

### 7. Documentation System (`docs/` module)
- **Internal Documentation**: Separate from Sphinx docs
- **MCP Instructions**: Loaded dynamically into the server
- **Centralized Management**: All MCP-specific documentation in one place

## Key Design Patterns

### 1. Layered Architecture
```
MCP Client → tools.py (MCP Layer) → sa/ (Core Layer) → SQLAlchemy → Database
```

### 2. Configuration Management
- Environment variable → JSON config file → Cached objects
- Separation of configuration loading and usage

### 3. Data Models
- Pydantic models for type safety and validation
- Structured data exchange between layers

## Current Capabilities

### Implemented
- Database schema introspection with full metadata
- Support for any SQLAlchemy-compatible database
- MCP protocol integration via FastMCP
- Configuration management system

### Planned (Based on Project Goals)
- Query execution with result optimization
- Data pagination to prevent large data loads to LLMs
- Data export to local files
- Access control features
- Configurable tool exposure (enable/disable specific tools)
- Query optimization and caching

## Development Guidelines

### Adding New MCP Tools
1. Implement core functionality in appropriate `sa/` module
2. Create wrapper function in `tools.py` with `@mcp.tool()` decorator
3. Import the tool in `create_app.py` to register it

### Configuration Changes
1. Update the configuration schema in `config.py`
2. Ensure backward compatibility with existing config files
3. Update documentation and examples

### Database Operations
1. All SQL operations should go through the `sa/` module
2. Use SQLAlchemy's reflection and metadata capabilities
3. Implement proper error handling and connection management

## Installation Modes (Future)

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
