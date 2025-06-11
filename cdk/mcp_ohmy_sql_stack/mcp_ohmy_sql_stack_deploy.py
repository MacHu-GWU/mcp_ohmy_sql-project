# -*- coding: utf-8 -*-

from mcp_ohmy_sql.tests.aws.stack_ctx_enum import stack_ctx_enum

# --- 📦 cdk synth
# stack_ctx_enum.my_ohmy_sql_dev.cdk_synth(dir_cdk=__file__)

# --- 🔍 cdk diff
# stack_ctx_enum.my_ohmy_sql_dev.cdk_diff(dir_cdk=__file__)

# --- 🚀 cdk deploy
stack_ctx_enum.my_ohmy_sql_dev.cdk_deploy(dir_cdk=__file__, prompt=False)

# --- 💥 cdk destroy
# stack_ctx_enum.my_ohmy_sql_dev.cdk_destroy(dir_cdk=__file__, prompt=False)