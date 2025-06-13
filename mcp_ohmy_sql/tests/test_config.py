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
    BotoSessionKwargs,
    AWSRedshiftConnection,
    Database,
    Config,
)

from .chinook.chinook_data_file import path_Chinook_Sqlite_sqlite
from .aws.constants import aws_profile, database_name, workgroup_name


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
    chinook_redshift = Database(
        identifier="chinook redshift",
        description="Chinook is a sample database available for SQL Server, Oracle, MySQL, etc. It can be created by running a single SQL script. Chinook database is an alternative to the Northwind database, being ideal for demos and testing ORM tools targeting single and multiple database servers.",
        db_type="postgres",
        connection=AWSRedshiftConnection(
            boto_session_kwargs=BotoSessionKwargs(profile_name=aws_profile),
            redshift_connector_kwargs=dict(
                iam=True,
                database=database_name,
                is_serverless=True,
                serverless_work_group=workgroup_name,
                profile=aws_profile,
                timeout=10,
            ),
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
    databases.append(DatabaseEnum.chinook_redshift)

config = Config(
    version="0.1.1",
    settings=Settings(),
    databases=databases,
)
