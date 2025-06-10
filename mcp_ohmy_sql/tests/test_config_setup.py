# -*- coding: utf-8 -*-


import json
from mcp_ohmy_sql.tests.config import path_sample_config, config


path_sample_config.write_text(
    json.dumps(
        config.model_dump(),
        indent=4,
        ensure_ascii=False,
    ),
)
