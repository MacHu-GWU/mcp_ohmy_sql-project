# -*- coding: utf-8 -*-

import json
from pathlib import Path

from mcp_ohmy_sql.tests.config import config, chinook_db
from mcp_ohmy_sql.sa.api import SchemaInfo, encode_schema_info

dir_here = Path(__file__).absolute().parent
path_hierarchy_encoded = dir_here / "01_hierarchy_encoded.txt"
path_json_encoded_formatted = dir_here / "02_json_encoded_formatted.json"
path_json_encoded_compact = dir_here / "03_json_encoded_compact.json"

schema_info = SchemaInfo.from_metadata(
    engine=chinook_db.sa_engine,
    metadata=chinook_db.sa_metadata,
    schema_name=None,
)
encode_schema_info(schema_info)
s = config.get_database_schema()
path_hierarchy_encoded.write_text(s)

dct = schema_info.model_dump(exclude_none=True)
path_json_encoded_formatted.write_text(json.dumps(dct, indent=4))
path_json_encoded_compact.write_text(json.dumps(dct))