# -*- coding: utf-8 -*-

"""

"""

import json
from mcp_ohmy_sql.tests.test_database_setup import DBUrlEnum
from mcp_ohmy_sql.paths import path_config

dct = {
    "version": "0.1.1",
    "settings": {},
    "databases": [
        {
            "identifier": "chinook sqlite",
            "description": "Chinook is a sample database available for SQL Server, Oracle, MySQL, etc. It can be created by running a single SQL script. Chinook database is an alternative to the Northwind database, being ideal for demos and testing ORM tools targeting single and multiple database servers.",
            "connection": {
                "type": "sqlalchemy",
                "create_engine_kwargs": {"url": DBUrlEnum.sqlite},
            },
            "schemas": [
                {
                    "table_filter": {
                        "include": [],
                        "exclude": ["Playlist", "PlaylistTrack"],
                    }
                }
            ],
        },
        {
            "identifier": "chinook postgres",
            "description": "Chinook is a sample database available for SQL Server, Oracle, MySQL, etc. It can be created by running a single SQL script. Chinook database is an alternative to the Northwind database, being ideal for demos and testing ORM tools targeting single and multiple database servers.",
            "connection": {
                "type": "sqlalchemy",
                "create_engine_kwargs": {"url": DBUrlEnum.postgres},
            },
            "schemas": [
                {
                    "table_filter": {
                        "include": [],
                        "exclude": ["Playlist", "PlaylistTrack"],
                    }
                }
            ],
        },
    ],
}
path_config.write_text(json.dumps(dct, indent=4, ensure_ascii=False))
