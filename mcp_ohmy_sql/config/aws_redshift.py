# -*- coding: utf-8 -*-

"""
AWS Redshift connection configuration.
"""

import typing as T
from functools import cached_property

from enum_mate.api import BetterStrEnum
from pydantic import Field, field_validator

from ..lazy_import import sa, BotoSesManager, redshift_connector, aws_rs
from ..constants import ConnectionTypeEnum

from .conn import BaseConnection
from .boto_session import BotoSessionKwargs


class AwsRedshiftConnectionMethodEnum(BetterStrEnum):
    """
    Supported connection methods for AWS Redshift.
    """
    redshift_connector = "redshift_connector"
    sqlalchemy = "sqlalchemy"


class AWSRedshiftConnection(BaseConnection):
    """
    Configures AWS Redshift connections for data warehouse access.
    
    Provides multiple connection methods for different Redshift deployment types:
    
    :param type: DO NOT set this field manually, it is automatically set to "aws_redshift".
    :param method: Connection library to use - "redshift_connector" or "sqlalchemy"
    
    **Direct Connection Parameters (username/password authentication):**
    
    :param host: Redshift cluster endpoint hostname
    :param port: Redshift cluster port (usually 5439)
    :param database: Target database name
    :param username: Database username
    :param password: Database password
    
    **IAM-based Authentication for Redshift Cluster:**
    
    :param cluster_identifier: Redshift cluster identifier for IAM authentication
    :param database: Target database name
    :param boto_session_kwargs: AWS credentials and session configuration
    
    **IAM-based Authentication for Redshift Serverless:**
    
    :param namespace_name: Redshift Serverless namespace name
    :param workgroup_name: Redshift Serverless workgroup name
    :param boto_session_kwargs: AWS credentials and session configuration
    
    **Additional Configuration:**
    
    :param redshift_connector_kwargs: Additional parameters for the redshift-connector library
    """
    # fmt: off
    type: T.Literal["aws_redshift"] = Field(default=ConnectionTypeEnum.AWS_REDSHIFT.value)
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
    # fmt: on

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
        """
        Returns a Redshift connection object using the redshift_connector library.
        """
        return redshift_connector.connect(
            **self.redshift_connector_kwargs,
        )

    @cached_property
    def rs_conn(self) -> "redshift_connector.Connection":
        """
        Returns a cached Redshift connection object using the redshift_connector library.
        """
        return self.get_rs_conn()

    def get_sa_engine(self) -> "sa.Engine":
        """
        Returns a SQLAlchemy engine for connecting to AWS Redshift.
        """
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
        """
        Returns a cached SQLAlchemy engine for connecting to AWS Redshift.
        """
        return self.get_sa_engine()
