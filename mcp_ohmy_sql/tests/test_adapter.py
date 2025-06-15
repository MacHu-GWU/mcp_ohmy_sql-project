# -*- coding: utf-8 -*-

from which_runtime.api import runtime

from ..adapter.api import Adapter
from .test_config import DatabaseEnum, test_config

test_adapter = Adapter(config=test_config)

from .chinook.chinook_data_model import Base
from .setup_relational_database import setup_relational_database

sqlite_database = DatabaseEnum.chinook_sqlite
setup_relational_database(
    engine=sqlite_database.sa_engine,
    metadata=Base.metadata,
    db_type=sqlite_database.db_type_enum,
)

if runtime.is_local_runtime_group:
    pass
