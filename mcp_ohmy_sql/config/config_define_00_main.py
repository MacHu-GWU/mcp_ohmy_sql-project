# -*- coding: utf-8 -*-

import typing as T
import json
from pathlib import Path
from functools import cached_property

from pydantic import BaseModel, Field

try:
    import sqlalchemy as sa
except ImportError:  # pragma: no cover
    pass

from .config_define_01_database_schema import ConfigDatabaseSchemaMixin


class Settings(BaseModel):
    pass


class TableFilter(BaseModel):
    include: list[str] = Field(default_factory=list)
    exclude: list[str] = Field(default_factory=list)


class Schema(BaseModel):
    name: T.Optional[str] = Field(default=None)
    table_filter: TableFilter = Field(default_factory=TableFilter)


class BaseConnection(BaseModel):
    type: str = Field()


class SqlalchemyConnection(BaseConnection):
    type: T.Literal["sqlalchemy"] = Field(default="sqlalchemy")
    create_engine_kwargs: dict[str, T.Any] = Field(default_factory=dict)

    @cached_property
    def sa_engine(self) -> "sa.Engine":
        return sa.create_engine(**self.create_engine_kwargs)


class Database(BaseModel):
    identifier: str = Field()
    description: str = Field(default="")
    connection: T.Union[SqlalchemyConnection] = Field(
        discriminator="type",
    )
    schemas: list[Schema] = Field()

    @cached_property
    def schemas_mapping(self) -> dict[str, Schema]:
        """
        Create a mapping of schema names to Schema objects.
        """
        return {schema.name: schema for schema in self.schemas}

    @cached_property
    def sa_engine(self) -> "sa.Engine":
        return self.connection.sa_engine

    @cached_property
    def sa_metadata(self) -> "sa.MetaData":
        metadata = sa.MetaData()
        for schema in self.schemas:
            metadata.reflect(
                self.sa_engine,
                schema=schema.name,
                views=True,
            )
        return metadata


class Config(
    BaseModel,
    ConfigDatabaseSchemaMixin,
):
    version: str = Field()
    settings: Settings = Field(default_factory=Settings)
    databases: list[Database] = Field()

    @classmethod
    def load(cls, path: Path):
        """
        Load configuration from a JSON file.
        """
        return cls(**json.loads(path.read_text()))

    @cached_property
    def databases_mapping(self) -> dict[str, Database]:
        """
        Create a mapping of database identifiers to Database objects.
        """
        return {db.identifier: db for db in self.databases}
