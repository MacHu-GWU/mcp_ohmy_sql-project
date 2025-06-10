# -*- coding: utf-8 -*-

from mcp_ohmy_sql.config.config_define_00_main import (
    Settings,
    TableFilter,
    Schema,
    SqlalchemyConnection,
    Database,
    Config,
)
from mcp_ohmy_sql.paths import path_sample_config

from rich import print as rprint


class TestConfig:
    def test_seder(self):
        config = Config(
            version="0.1.1",
            settings=Settings(),
            databases=[
                Database(
                    identifier="chinook_sqlite",
                    description="...",
                    connection=SqlalchemyConnection(
                        create_engine_kwargs={"url": "..."},
                    ),
                    schemas=[
                        Schema(
                            name="public",
                            table_filter=TableFilter(
                                include=[],
                                exclude=[],
                            ),
                        )
                    ],
                )
            ],
        )
        dct = config.model_dump()
        config_1 = Config(**dct)
        dct_1 = config_1.model_dump()
        assert dct == dct_1
        assert config == config_1

        minimal_dct = {
            "version": "0.1.1",
            "databases": [
                {
                    "identifier": "chinook_sqlite",
                    "connection": {
                        "type": "sqlalchemy",
                        "create_engine_kwargs": {"url": "..."},
                    },
                    "schemas": [{}],
                }
            ],
        }
        config = Config(**minimal_dct)
        # rprint(config)  # for debug only

    def test_load(self):
        config = Config.load(path_sample_config)
        # rprint(config)  # for debug only

        for database_name, database in config.databases_mapping.items():
            # rprint(f"{database = }")  # for debug only
            for schema_name, schema in database.schemas_mapping.items():
                # rprint(f"{schema = }")  # for debug only
                pass


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.config.config_define_00_main.py",
        preview=False,
    )
