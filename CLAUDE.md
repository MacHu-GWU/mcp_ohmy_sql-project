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
- Environment-driven configuration via `FINAL_SQL_MCP_CONFIG`
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

## Testing Strategy

- Unit tests for core SQL operations in `mcp_ohmy_sql/tests/`
- Integration tests for MCP tool functionality in `tests/`
- Test database provided via `tests/chinook.py`

This architecture ensures modularity, testability, and easy extension while maintaining clear separation between MCP protocol handling and database operations.