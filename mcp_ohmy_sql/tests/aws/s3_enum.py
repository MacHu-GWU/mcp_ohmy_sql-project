# -*- coding: utf-8 -*-

from functools import cached_property
from s3pathlib import S3Path, context
from .bsm_enum import BsmEnum


class _S3Enum:
    @cached_property
    def bsm(self):
        bsm = BsmEnum.bsm
        context.attach_boto_session(bsm.boto_ses)
        return bsm

    @cached_property
    def s3dir_root(self) -> S3Path:
        return S3Path(
            f"s3://{self.bsm.aws_account_alias}-{self.bsm.aws_region}-data"
            f"/projects/mcp-ohmy-sql/"
        ).to_dir()

    @cached_property
    def s3dir_tests(self) -> S3Path:
        return self.s3dir_root.joinpath("tests").to_dir()

    @cached_property
    def s3dir_tests_aws_redshift_staging(self) -> S3Path:
        return self.s3dir_tests.joinpath("aws_redshift", "staging").to_dir()


S3Enum = _S3Enum()
