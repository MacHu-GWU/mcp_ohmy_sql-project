# -*- coding: utf-8 -*-

from mcp_ohmy_sql.aws.aws_redshift import api


def test():
    _ = api


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.aws.aws_redshift.api",
        preview=False,
    )
