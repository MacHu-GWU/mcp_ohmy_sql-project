# Code Structure Guide for mcp_ohmy_sql

This document provides a comprehensive guide to the codebase structure and architecture of the mcp_ohmy_sql project.

## Overview

mcp_ohmy_sql is a Model Context Protocol (MCP) server that provides SQL database capabilities through SQLAlchemy. The project follows a modular architecture with clear separation of concerns between database operations, MCP tool definitions, and server configuration.

## Project Structure

```
mcp_ohmy_sql/
├── __init__.py              # Package initialization
├── _version.py              # Version information
├── api.py                   # API definitions (future use)
├── config.py                # Configuration management
├── config_init.py           # Configuration initialization
├── constants.py             # Project constants
├── create_app.py            # FastAPI server factory
├── paths.py                 # Path utilities
├── server.py                # MCP server definition
├── tools.py                 # MCP tool implementations (wrapper layer)
├── sa/                      # SQLAlchemy core implementation
│   ├── __init__.py
│   └── metadata.py          # Database schema introspection
├── tests/                   # Internal tests
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
- Defines the FastMCP server instance using `@mcp.server()`
- Currently basic setup with server name and empty instructions
- Entry point for all MCP tool registrations

### 4. Configuration System (`config.py`, `config_init.py`)
- Environment-driven configuration via `MCP_OHMY_SQL_CONFIG`
- JSON-based configuration file format
- Provides cached SQLAlchemy engine and metadata objects
- Configuration schema:
  ```json
  {
    "version": "0.1.1",
    "db_url": "sqlite:////path/to/database.sqlite", 
    "db_schema": "optional_schema_name"
  }
  ```

### 5. MCP Tools Layer (`tools.py`)
- **Purpose**: Wrapper layer that converts SQLAlchemy operations into MCP tools
- **Current Tools**: 
  - `get_database_schema_info()`: Database schema introspection
- **Design Pattern**: Each function decorated with `@mcp.tool()` becomes an available MCP tool
- **Data Flow**: tools.py → sa/ module → SQLAlchemy → Database

### 6. SQLAlchemy Core (`sa/` module)
- **Purpose**: Raw SQLAlchemy implementation providing core SQL capabilities
- **`sa/__init__.py`**: Module initialization and imports
- **`sa/metadata.py`**: Database schema introspection implementation
  - Pydantic models for structured data (`ForeignKeyInfo`, `ColumnInfo`, `TableInfo`, `SchemaInfo`)
  - `get_database_schema_info()`: Core function that reflects database metadata
  - Comprehensive schema analysis including tables, columns, keys, and relationships

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
