# -*- coding: utf-8 -*-

from claude_desktop_config.api import ClaudeDesktopConfig, Mcp, BaseMcpEnum

cdc = ClaudeDesktopConfig()


class MCPEnum(BaseMcpEnum):
    OHMY_SQL = Mcp(
        name="OhMySql",
        settings={
            "command": "/Users/sanhehu/Documents/GitHub/mcp_ohmy_sql-project/.venv/bin/python",
            "args": [
                "/Users/sanhehu/Documents/GitHub/mcp_ohmy_sql-project/app.py",
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
    MCPEnum.OHMY_SQL,
    # MCPEnum.NEON,
}
MCPEnum.apply(wanted_mcps, cdc)
