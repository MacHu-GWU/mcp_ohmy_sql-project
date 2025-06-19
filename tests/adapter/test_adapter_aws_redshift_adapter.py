# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.test_config import DatabaseEnum

try:
    from rich import print as rprint
except ImportError:  # pragma: no cover
    pass


class TestAwsRedshiftAdapterMixin:
    def test_get_relational_database_info(
        self,
        mcp_ohmy_sql_config,
        mcp_ohmy_sql_adapter,
    ):
        database = mcp_ohmy_sql_config.databases_mapping[
            DatabaseEnum.chinook_redshift.identifier
        ]
        database_info = mcp_ohmy_sql_adapter.get_aws_redshift_database_info(database)
        # rprint(database_info)  # for debug only


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.adapter.aws_redshift_adapter.py",
        preview=False,
    )
