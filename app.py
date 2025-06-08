# -*- coding: utf-8 -*-

from mcp_ohmy_sql.create_app import create_app

mcp = create_app()

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
