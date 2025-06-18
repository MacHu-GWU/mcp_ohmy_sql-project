# -*- coding: utf-8 -*-

import typing as T
from functools import cached_property

from pydantic import Field

from ..lazy_import import sa
from ..constants import ConnectionTypeEnum

from .conn import BaseConnection


class SqlalchemyConnection(BaseConnection):
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
        return sa.create_engine(self._url, **self.create_engine_kwargs)
