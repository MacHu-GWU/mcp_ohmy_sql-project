# -*- coding: utf-8 -*-

import pytest
from which_runtime.api import runtime
from mcp_ohmy_sql.db.aws_redshift.schema_3_extractor import (
    SchemaTableFilter,
    new_database_info,
)
from mcp_ohmy_sql.tests.test_config import DatabaseEnum
from rich import print as rprint


@pytest.mark.skipif(
    runtime.is_local_runtime_group is False,
    reason="only run on local runtime",
)
def test_new_column_info(
    rs_conn,
    rs_engine,
    rs_tables,
    rs_data,
):
    database = DatabaseEnum.chinook_redshift
    schema = database.schemas[0]

    def _new_database_info(conn_or_engine):
        return new_database_info(
            conn_or_engine=conn_or_engine,
            db_name=database.identifier,
            schema_table_filter_list=[
                SchemaTableFilter(
                    schema_name=schema.name,
                    include=schema.table_filter.include,
                    exclude=schema.table_filter.exclude,
                )
            ],
        )

    database_info = _new_database_info(rs_conn)
    rprint(database_info)  # pragma: no cover

    database_info = _new_database_info(rs_engine)
    rprint(database_info)  # pragma: no cover


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.db.aws_redshift.schema_3_extractor.py",
        preview=False,
    )
