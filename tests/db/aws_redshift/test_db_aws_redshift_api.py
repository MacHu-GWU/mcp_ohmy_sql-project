# -*- coding: utf-8 -*-

from mcp_ohmy_sql.db.aws_redshift import api


def test():
    _ = api
    _ = api.ColumnInfo
    _ = api.TableInfo
    _ = api.SchemaInfo
    _ = api.DatabaseInfo
    _ = api.encode_column_info
    _ = api.encode_table_info
    _ = api.encode_schema_info
    _ = api.encode_database_info
    _ = api.RedshiftDataTypeEnum
    _ = api.REDSHIFT_TYPE_TO_LLM_TYPE_MAPPING
    _ = api.redshift_type_to_llm_type
    _ = api.SchemaTableFilter
    _ = api.new_database_info


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.db.aws_redshift.api",
        preview=False,
    )
