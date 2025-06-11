# -*- coding: utf-8 -*-

"""
This script sets up a test configuration for testing purposes.
"""


from which_runtime.api import runtime

from ..config.config_define import (
    Settings,
    TableFilter,
    Schema,
    SqlalchemyConnection,
    Database,
    Config,
)

from .chinook import path_Chinook_Sqlite_sqlite


# os.environ[EnvVarEnum.MCP_OHMY_SQL_CONFIG.name] = str(path_sample_config)
class DatabaseEnum:
    chinook_sqlite = Database(
        identifier="chinook sqlite",
        description="Chinook is a sample database available for SQL Server, Oracle, MySQL, etc. It can be created by running a single SQL script. Chinook database is an alternative to the Northwind database, being ideal for demos and testing ORM tools targeting single and multiple database servers.",
        db_type="sqlite",
        connection=SqlalchemyConnection(
            create_engine_kwargs={"url": f"sqlite:///{path_Chinook_Sqlite_sqlite}"},
        ),
        schemas=[
            Schema(
                table_filter=TableFilter(
                    include=[],
                    exclude=["Playlist", "PlaylistTrack"],
                )
            )
        ],
    )
    chinook_postgres = Database(
        identifier="chinook postgres",
        description="Chinook is a sample database available for SQL Server, Oracle, MySQL, etc. It can be created by running a single SQL script. Chinook database is an alternative to the Northwind database, being ideal for demos and testing ORM tools targeting single and multiple database servers.",
        db_type="postgres",
        connection=SqlalchemyConnection(
            create_engine_kwargs={
                "url": "postgresql+psycopg2://postgres:password@localhost:40311/postgres",
            }
        ),
        schemas=[
            Schema(
                table_filter=TableFilter(
                    include=[],
                    exclude=["Playlist", "PlaylistTrack"],
                )
            )
        ],
    )


databases = [
    DatabaseEnum.chinook_sqlite,
]

# we only use sqlite in CI test runtime
if runtime.is_local_runtime_group:
    databases.append(DatabaseEnum.chinook_postgres)

config = Config(
    version="0.1.1",
    settings=Settings(),
    databases=databases,
)
