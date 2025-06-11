#!/usr/bin/env python3

from mcp_ohmy_sql.tests.aws.stack_enum import stack_enum

_ = stack_enum.my_ohmy_sql_dev

stack_enum.app.synth()
