# -*- coding: utf-8 -*-

# uncomment this line when running this directly in venv Python
from mcp_ohmy_sql.create_app import create_app


def main():
    """Main entry point for the MCP server."""
    mcp = create_app()
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
