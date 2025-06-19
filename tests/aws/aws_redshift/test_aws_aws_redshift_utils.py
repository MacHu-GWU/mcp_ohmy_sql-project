# -*- coding: utf-8 -*-

from mcp_ohmy_sql.aws.aws_redshift.utils import (
    Session,
    execute_many_sql,
)

import pytest
from which_runtime.api import runtime
from mcp_ohmy_sql.tests.test_config import DatabaseEnum

database = DatabaseEnum.chinook_redshift


@pytest.mark.skipif(
    condition=runtime.is_local_runtime_group is False,
    reason="only run on local runtime",
)
def test_execute_many_sql():
    sql = "SELECT 1 AS value;"

    conn = database.connection.get_rs_conn()
    execute_many_sql(
        conn_or_engine=conn,
        sql=sql,
    )
    conn.close()

    execute_many_sql(
        conn_or_engine=database.connection.sa_engine,
        sql=sql,
    )


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.aws.aws_redshift.utils",
        preview=False,
    )
