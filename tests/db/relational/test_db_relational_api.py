# -*- coding: utf-8 -*-

from mcp_ohmy_sql.db.relational import api


def test():
    _ = api
    _ = api.ForeignKeyInfo
    _ = api.ColumnInfo
    _ = api.TableInfo
    _ = api.SchemaInfo
    _ = api.DatabaseInfo
    _ = api.SQLALCHEMY_TYPE_MAPPING
    _ = api.sqlalchemy_type_to_llm_type
    _ = api.new_foreign_key_info
    _ = api.new_column_info
    _ = api.new_table_info
    _ = api.new_schema_info
    _ = api.new_database_info
    _ = api.encode_column_info
    _ = api.TABLE_TYPE_NAME_MAPPING
    _ = api.encode_table_info
    _ = api.encode_schema_info
    _ = api.encode_database_info


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.db.relational.api",
        preview=False,
    )
