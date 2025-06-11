# -*- coding: utf-8 -*-

from pathlib import Path
from claude_desktop_config.api import ClaudeDesktopConfig, Mcp, BaseMcpEnum
from mcp_ohmy_sql.paths import dir_venv_bin, dir_unit_test, path_sample_config


cdc = ClaudeDesktopConfig()


dir_home = Path.home()


class MCPEnum(BaseMcpEnum):
    OHMY_SQL_DEV = Mcp(
        name="OhMySqlDev",
        settings={
            "command": f"{dir_venv_bin}/python",
            "args": [
                f"{dir_unit_test}/app.py",
            ],
            "env": {
                "MCP_OHMY_SQL_CONFIG": f"{path_sample_config}",
            },
        },
    )
    OHMY_SQL_UVX = Mcp(
        name="OhMySql",
        settings={
            "command": f"{dir_home}/.pyenv/shims/uvx",
            "args": [
                "--with",
                # "mcp-ohmy-sql[sqlite,postgres]",  # you can add ==${version} if you want to specify a version
                "mcp-ohmy-sql[sqlite,postgres]==0.1.2.dev2",  # you can add ==${version} if you want to specify a version
                "mcp-ohmy-sql",
            ],
            "env": {
                "MCP_OHMY_SQL_CONFIG": f"{path_sample_config}",
            },
        },
    )


wanted_mcps = {
    # MCPEnum.OHMY_SQL_DEV,
    MCPEnum.OHMY_SQL_UVX,
}
MCPEnum.apply(wanted_mcps, cdc)
