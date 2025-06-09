# -*- coding: utf-8 -*-

from mcp.server.fastmcp import FastMCP

from .docs import doc_files

mcp = FastMCP(
    name="Final SQL MCP Server",
    instructions=doc_files.mcp_instructions,
)
