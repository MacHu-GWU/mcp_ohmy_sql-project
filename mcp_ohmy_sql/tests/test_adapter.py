# -*- coding: utf-8 -*-

from which_runtime.api import runtime

from ..adapter.api import Adapter
from .test_config import DatabaseEnum, test_config

test_adapter = Adapter(config=test_config)

# prepare test database
from .chinook.chinook_data_model import Base
from .setup_relational_database import setup_relational_database
from .setup_aws_redshift_database import setup_aws_redshift_database

sqlite_database = DatabaseEnum.chinook_sqlite
setup_relational_database(
    engine=sqlite_database.connection.sa_engine,
    metadata=Base.metadata,
    db_type=sqlite_database.db_type_enum,
)

# if runtime.is_local_runtime_group:
#     postgres_database = DatabaseEnum.chinook_postgres
#     setup_relational_database(
#         engine=postgres_database.connection.sa_engine,
#         metadata=Base.metadata,
#         db_type=postgres_database.db_type_enum,
#     )
#     redshift_database = DatabaseEnum.chinook_redshift
#     setup_aws_redshift_database(conn_or_engine=redshift_database.connection.sa_engine)
