# -*- coding: utf-8 -*-

import typing as T
import json
from pathlib import Path
from functools import cached_property

from pydantic import BaseModel, Field, field_validator

from ..constants import DbTypeEnum

try:
    import sqlalchemy as sa
except ImportError:  # pragma: no cover
    pass
try:
    from boto_session_manager import BotoSesManager
except ImportError:  # pragma: no cover
    pass
try:
    import redshift_connector
    import simple_aws_redshift.api as aws_rs
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


from .sqlalchemy import SqlalchemyConnection
from .aws_redshift import AWSRedshiftConnection

T_CONNECTION = T.Union[
    SqlalchemyConnection,
    AWSRedshiftConnection,
]


class Database(BaseModel):
    identifier: str = Field()
    description: str = Field(default="")
    db_type: str = Field()
    connection: T_CONNECTION = Field(discriminator="type")
    schemas: list[Schema] = Field()

    @field_validator("db_type", mode="after")
    @classmethod
    def check_name(cls, value: str) -> str:  # pragma: no cover
        if DbTypeEnum.is_valid_value(value) is False:
            raise ValueError(f"{value} is not a valid value of {DbTypeEnum}")
        return value

    @property
    def db_type_enum(self) -> DbTypeEnum:
        """
        Get the database type as an enum.
        """
        return DbTypeEnum.get_by_value(self.db_type)

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
