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


T_DB_TYPE = T.Literal[
    "sqlite",
    "postgres",
    "mysql",
    "mssql",
    "oracle",
    "aws_redshift",
    "aws_redshift_data_api",
    "aws_athena",
    "aws_opensearch",
    "aws_s3_data_file",
    "elasticsearch",
    "opensearch",
    "duckdb",
]


class Database(BaseModel):
    identifier: str = Field()
    description: str = Field(default="")
    db_type: T_DB_TYPE = Field()
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


class Config(BaseModel):
    version: str = Field()
    settings: Settings = Field(default_factory=Settings)
    databases: list[Database] = Field()

    @classmethod
    def load(cls, path: Path):
        """
        Load configuration from a JSON file.
        """
        try:
            s = path.read_text()
        except Exception as e:  # pragma: no cover
            raise Exception(
                f"Failed to read configuration content from {path}! Error: {e!r}"
            )

        try:
            dct = json.loads(s)
        except Exception as e:  # pragma: no cover
            raise Exception(
                f"Failed to load configuration from {path}! Check your JSON content! Error: {e!r}"
            )

        try:
            config = cls(**dct)
        except Exception as e:  # pragma: no cover
            raise Exception(
                f"Configuration Validation failed! Check your JSON content! Error: {e!r}"
            )

        return config

    @cached_property
    def databases_mapping(self) -> dict[str, Database]:
        """
        Create a mapping of database identifiers to Database objects.
        """
        return {db.identifier: db for db in self.databases}
