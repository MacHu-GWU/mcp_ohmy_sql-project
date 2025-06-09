# -*- coding: utf-8 -*-

from mcp_ohmy_sql.sa import api


def test():
    _ = api
    _ = api.SQLALCHEMY_TYPE_MAPPING
    _ = api.ColumnType
    _ = api.ForeignKeyInfo
    _ = api.ColumnInfo
    _ = api.TableInfo
    _ = api.SchemaInfo
    _ = api.encode_column_info
    _ = api.TABLE_TYPE_NAME_MAPPING
    _ = api.encode_table_info
    _ = api.encode_schema_info
    _ = api.execute_count_query
    _ = api.execute_select_query


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.sa.api",
        preview=False,
    )
