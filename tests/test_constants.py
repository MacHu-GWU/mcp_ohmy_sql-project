# -*- coding: utf-8 -*-

import os
from mcp_ohmy_sql.constants import EnvVar


class TestEnvVar:
    def test_value(self):
        name = "TEST_ENV_VAR"
        env_var = EnvVar(name=name)
        assert env_var.value == ""

        os.environ[name] = "MY_TEST_ENV_VAR_VALUE"
        assert env_var.value == "MY_TEST_ENV_VAR_VALUE"


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.constants",
        preview=False,
    )
