# -*- coding: utf-8 -*-

import typing as T
from functools import cached_property

from enum_mate.api import BetterStrEnum
from pydantic import Field, field_validator

from ..lazy_import import sa, BotoSesManager, redshift_connector, aws_rs

from .conn import BaseConnection, BotoSessionKwargs


class AwsRedshiftConnectionMethodEnum(BetterStrEnum):
    redshift_connector = "redshift_connector"
    sqlalchemy = "sqlalchemy"


class AWSRedshiftConnection(BaseConnection):
    type: T.Literal["aws_redshift"] = Field(default="aws_redshift")
    method: str = Field()
    host: T.Optional[str] = Field(default=None)
    port: T.Optional[int] = Field(default=None)
    database: T.Optional[str] = Field(default=None)
    username: T.Optional[str] = Field(default=None)
    password: T.Optional[str] = Field(default=None)
    cluster_identifier: T.Optional[str] = Field(default=None)
    namespace_name: T.Optional[str] = Field(default=None)
    workgroup_name: T.Optional[str] = Field(default=None)
    boto_session_kwargs: T.Optional["BotoSessionKwargs"] = Field(default=None)
    redshift_connector_kwargs: T.Optional[dict[str, T.Any]] = Field(default=None)

    @field_validator("method", mode="after")
    @classmethod
    def check_method(cls, value: str) -> str:  # pragma: no cover
        if AwsRedshiftConnectionMethodEnum.is_valid_value(value) is False:
            raise ValueError(
                f"{value} is not a valid value of {AwsRedshiftConnectionMethodEnum}"
            )
        return value

    @cached_property
    def bsm(self) -> "BotoSesManager":
        return self.boto_session_kwargs.get_bsm()

    @cached_property
    def _use_what(self) -> T.Literal["redshift_connector", "sqlalchemy"]:
        raise NotImplementedError

    def get_rs_conn(self) -> "redshift_connector.Connection":
        return redshift_connector.connect(
            **self.redshift_connector_kwargs,
        )

    @cached_property
    def rs_conn(self) -> "redshift_connector.Connection":
        return self.get_rs_conn()

    def get_sa_engine(self) -> "sa.Engine":
        if (
            (self.host is not None)
            and (self.port is not None)
            and (self.database is not None)
            and (self.username is not None)
            and (self.password is not None)
        ):
            params = aws_rs.RedshiftClusterConnectionParams(
                host=self.host,
                port=self.port,
                database=self.database,
                username=self.username,
                password=self.password,
            )
            return params.get_engine()

        # Redshift Cluster with IAM
        if (
            (self.cluster_identifier is not None)
            and (self.database is not None)
            and (self.boto_session_kwargs is not None)
        ):
            params = aws_rs.RedshiftClusterConnectionParams.new(
                redshift_client=self.bsm.redshift_client,
                cluster_identifier=self.cluster_identifier,
                db_name=self.database,
            )
            return params.get_engine()

        # Redshift Serverless with IAM
        if (
            (self.namespace_name is not None)
            and (self.workgroup_name is not None)
            and (self.boto_session_kwargs is not None)
        ):
            params = aws_rs.RedshiftServerlessConnectionParams.new(
                redshift_serverless_client=self.bsm.redshiftserverless_client,
                namespace_name=self.namespace_name,
                workgroup_name=self.workgroup_name,
            )
            return params.get_engine()

        raise ValueError("Cannot create SQLAlchemy engine for AWS Redshift")

    @cached_property
    def sa_engine(self) -> "sa.Engine":
        return self.get_sa_engine()
