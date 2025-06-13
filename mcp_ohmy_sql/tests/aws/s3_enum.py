# -*- coding: utf-8 -*-

from s3pathlib import S3Path, context
from .bsm_enum import bsm_enum

bsm = bsm_enum.dev
context.attach_boto_session(bsm.boto_ses)
s3dir_root = S3Path(
    f"s3://{bsm.aws_account_alias}-{bsm.aws_region}-data" f"/projects/mcp-ohmy-sql/"
).to_dir()
s3dir_tests = s3dir_root.joinpath("tests").to_dir()

s3dir_tests_aws_redshift_staging = s3dir_tests.joinpath(
    "aws_redshift", "staging"
).to_dir()
