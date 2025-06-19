# -*- coding: utf-8 -*-

"""
定义了在测试中要使用的 mcp_ohmy_sql Config.

注意! 最终测试的时候的 Config 对象的实例用的不是这个模块中的 config 对象, 而是从
path_sample_config 中读取而来的. 这个模块中的 config 对象只是我们的 source of truth,
用于将指定的 Config 写入到 path_sample_config 中, 以便在后续的测试中使用.
"""

import json
import os
from which_runtime.api import runtime

from ..paths import path_sample_config
from ..constants import DbTypeEnum, EnvVarEnum
from ..config.api import (
    Settings,
    TableFilter,
    Schema,
    BotoSessionKwargs,
    SqlalchemyConnection,
    AwsRedshiftConnectionMethodEnum,
    AWSRedshiftConnection,
    Database,
    Config,
)

from .chinook.chinook_data_file import path_Chinook_Sqlite_sqlite
from .aws.constants import aws_profile, database_name, namespace_name, workgroup_name


class DatabaseEnum:
    """
    Enumerate all database config used in tests.
    """

    chinook_sqlite = Database(
        identifier="chinook sqlite",
        description="Chinook is a sample database available for SQL Server, Oracle, MySQL, etc. It can be created by running a single SQL script. Chinook database is an alternative to the Northwind database, being ideal for demos and testing ORM tools targeting single and multiple database servers.",
        db_type=DbTypeEnum.SQLITE.value,
        connection=SqlalchemyConnection(
            url=f"sqlite:///{path_Chinook_Sqlite_sqlite}",
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
        db_type=DbTypeEnum.POSTGRESQL.value,
        connection=SqlalchemyConnection(
            drivername="postgresql+psycopg2",
            username="postgres",
            password="password",
            host="localhost",
            port=40311,
            database="postgres",
        ),
        schemas=[
            Schema(
                name="public",
                table_filter=TableFilter(
                    include=[],
                    exclude=["Playlist", "PlaylistTrack"],
                ),
            )
        ],
    )
    chinook_redshift = Database(
        identifier="chinook redshift",
        description="Chinook is a sample database available for SQL Server, Oracle, MySQL, etc. It can be created by running a single SQL script. Chinook database is an alternative to the Northwind database, being ideal for demos and testing ORM tools targeting single and multiple database servers.",
        db_type=DbTypeEnum.AWS_REDSHIFT.value,
        connection=AWSRedshiftConnection(
            method=AwsRedshiftConnectionMethodEnum.sqlalchemy.value,
            boto_session_kwargs=BotoSessionKwargs(profile_name=aws_profile),
            namespace_name=namespace_name,
            workgroup_name=workgroup_name,
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
                name="public",
                table_filter=TableFilter(
                    include=[],
                    exclude=["Playlist", "PlaylistTrack"],
                ),
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

test_config = Config(
    version="0.1.1",
    settings=Settings(),
    databases=databases,
)


def setup_test_config():
    path_sample_config.write_text(
        json.dumps(
            test_config.model_dump(),
            indent=4,
            ensure_ascii=False,
        ),
    )
    os.environ[EnvVarEnum.MCP_OHMY_SQL_CONFIG.name] = str(path_sample_config)
