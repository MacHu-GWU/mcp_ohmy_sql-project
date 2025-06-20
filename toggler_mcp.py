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
    OHMY_SQL_PRE_RELEASE = Mcp(
        name="OhMySqlPreRelease",
        settings={
            "command": f"{dir_home}/.pyenv/shims/uvx",
            "args": [
                "--with",
                "mcp-ohmy-sql[sqlite,postgres,aws_redshift]==0.1.3.dev1",
                "mcp-ohmy-sql",
            ],
            "env": {
                "MCP_OHMY_SQL_CONFIG": f"{path_sample_config}",
            },
        },
    )
    OHMY_SQL = Mcp(
        name="OhMySql",
        settings={
            "command": f"{dir_home}/.pyenv/shims/uvx",
            "args": [
                "--with",
                "mcp-ohmy-sql[sqlite,postgres]",
                "mcp-ohmy-sql",
            ],
            "env": {
                "MCP_OHMY_SQL_CONFIG": f"{path_sample_config}",
            },
        },
    )


wanted_mcps = {
    # MCPEnum.OHMY_SQL_DEV,
    MCPEnum.OHMY_SQL_PRE_RELEASE,
    # MCPEnum.OHMY_SQL,
}
MCPEnum.apply(wanted_mcps, cdc)
