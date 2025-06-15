# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.test_config_1_define import DatabaseEnum

try:
    from rich import print as rprint
except ImportError:
    pass


class TestAdapter:
    def test_get_database_and_schema_object(
        self,
        adapter,
    ):
        # invalid database
        flag, msg, database, schema = adapter.get_database_and_schema_object(
            database_identifier="invalid database",
        )
        assert flag is False
        assert "Error: Database" in msg

        # invalid schema
        flag, msg, database, schema = adapter.get_database_and_schema_object(
            database_identifier=DatabaseEnum.chinook_sqlite.identifier,
            schema_name="invalid schema",
        )
        assert flag is False
        assert "Error: Schema" in msg

        # valid database and schema
        flag, msg, database, schema = adapter.get_database_and_schema_object(
            database_identifier=DatabaseEnum.chinook_sqlite.identifier,
        )
        assert flag is True
        assert database.identifier == DatabaseEnum.chinook_sqlite.identifier
        assert schema.name is None

        # rprint(database)  # for debug only
        # rprint(schema)  # for debug only


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.adapter.adapter.py",
        preview=False,
    )
