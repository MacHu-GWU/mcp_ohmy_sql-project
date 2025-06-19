# -*- coding: utf-8 -*-

import json
import sqlalchemy as sa
from pathlib import Path

from mcp_ohmy_sql.tests.test_config import DbTypeEnum, DatabaseEnum, setup_test_config
from mcp_ohmy_sql.tests.chinook.chinook_data_model import Base
from mcp_ohmy_sql.tests.setup_relational_database import (
    setup_relational_database,
)
from mcp_ohmy_sql.db.relational.api import (
    encode_schema_info,
    new_schema_info,
)
engine = sa.create_engine("sqlite:///:memory:")

setup_relational_database(
    engine=engine,
    metadata=Base.metadata,
    db_type=DbTypeEnum.SQLITE,
    drop_first=True,
)

# get the latest metadata with views
metadata = sa.MetaData()
metadata.reflect(engine, views=True)

schema_info = new_schema_info(
    engine=engine,
    metadata=metadata,
    schema_name=None,
)
s = encode_schema_info(schema_info)

dir_here = Path(__file__).absolute().parent
path_hierarchy_encoded = dir_here / "01_hierarchy_encoded.txt"
path_json_encoded_formatted = dir_here / "02_json_encoded_formatted.json"
path_json_encoded_compact = dir_here / "03_json_encoded_compact.json"

path_hierarchy_encoded.write_text(s)
dct = schema_info.model_dump(exclude_none=True)
path_json_encoded_formatted.write_text(json.dumps(dct, indent=4))
path_json_encoded_compact.write_text(json.dumps(dct))
