# -*- coding: utf-8 -*-

"""
SQLAlchemy connection configuration for universal database access.
"""

import typing as T
from functools import cached_property

from pydantic import Field

from ..lazy_import import sa
from ..constants import ConnectionTypeEnum

from .conn import BaseConnection


class SqlalchemyConnection(BaseConnection):
    """
    Configures SQLAlchemy connections to support any SQL database.
    
    Provides three connection methods:

    :param type: DO NOT set this field manually, it is automatically set to "sqlalchemy".
    :param url: hard-coded connection URL, e.g., "sqlite:///path/to/db.sqlite",
        see: https://docs.sqlalchemy.org/en/20/core/engines.html

    The following are ``sqlalchemy.URL`` parameters, which can be used to construct
    the URL dynamically: https://docs.sqlalchemy.org/en/20/core/engines.html#creating-urls-programmatically

    :param drivername: a `URL` class parameter
    :param username: a `URL` class parameter
    :param password: a `URL` class parameter
    :param host: a `URL` class parameter
    :param port: a `URL` class parameter
    :param database: a `URL` class parameter
    :param query: a `URL` class parameter

    :param create_engine_kwargs: additional keyword arguments for
        `sa.create_engine() <https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine>`_
    """
    type: T.Literal["sqlalchemy"] = Field(default=ConnectionTypeEnum.SQLALCHEMY.value)
    url: T.Optional[str] = Field(default=None)
    drivername: T.Optional[str] = Field(default=None)
    username: T.Optional[str] = Field(default=None)
    password: T.Optional[str] = Field(default=None)
    host: T.Optional[str] = Field(default=None)
    port: T.Optional[int] = Field(default=None)
    database: T.Optional[str] = Field(default=None)
    query: T.Optional[T.Mapping[str, T.Union[T.Sequence[str], str]]] = Field(
        default=None
    )
    create_engine_kwargs: dict[str, T.Any] = Field(default_factory=dict)

    @property
    def _url(self) -> T.Union[str, "sa.URL"]:
        if self.url is not None:
            return self.url
        if self.query is None:
            self.query = {}

        url = sa.URL.create(
            drivername=self.drivername,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            query=self.query,
        )
        return url

    @cached_property
    def sa_engine(self) -> "sa.Engine":
        """
        Create a SQLAlchemy engine using the provided URL and additional parameters.
        """
        return sa.create_engine(self._url, **self.create_engine_kwargs)
