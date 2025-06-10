# -*- coding: utf-8 -*-

from claude_desktop_config.api import ClaudeDesktopConfig, Mcp, BaseMcpEnum

cdc = ClaudeDesktopConfig()


class MCPEnum(BaseMcpEnum):
    OHMY_SQL_VENV = Mcp(
        name="OhMySqlVenv",
        settings={
            "command": "/Users/sanhehu/Documents/GitHub/mcp_ohmy_sql-project/.venv/bin/python",
            "args": [
                "/Users/sanhehu/Documents/GitHub/mcp_ohmy_sql-project/mcp_ohmy_sql/app.py",
            ],
            "env": {
                "MCP_OHMY_SQL_CONFIG": "/Users/sanhehu/Documents/GitHub/mcp_ohmy_sql-project/sample_mcp_ohmy_sql_config.json",
            },
        },
    )
    OHMY_SQL_UVX = Mcp(
        name="OhMySql",
        settings={
            "command": "/Users/sanhehu/.pyenv/shims/uvx",
            "args": [
                "--with",
                "mcp-ohmy-sql[postgres]==0.1.2.dev1",
                "mcp-ohmy-sql",
            ],
            "env": {
                "MCP_OHMY_SQL_CONFIG": "/Users/sanhehu/Documents/GitHub/mcp_ohmy_sql-project/sample_mcp_ohmy_sql_config.json",
            },
        },
    )
    NEON = Mcp(
        name="Neon",
        settings={
            "command": "npx",
            "args": ["-y", "mcp-remote", "https://mcp.neon.tech/sse"],
        },
    )

wanted_mcps = {
    MCPEnum.OHMY_SQL_VENV,
    # MCPEnum.OHMY_SQL_UVX,
    # MCPEnum.NEON,
}
MCPEnum.apply(wanted_mcps, cdc)
