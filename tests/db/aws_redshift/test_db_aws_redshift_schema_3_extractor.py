# -*- coding: utf-8 -*-

import pytest
from which_runtime.api import runtime
from mcp_ohmy_sql.db.aws_redshift.schema_3_extractor import (
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
):
    database_info = new_database_info(
        conn=rs_conn,
        db_name=DatabaseEnum.chinook_redshift.identifier,
    )
    # rprint(database_info)  # pragma: no cover


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.db.aws_redshift.schema_2_extractor.py",
        preview=False,
    )
