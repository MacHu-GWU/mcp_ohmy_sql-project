# -*- coding: utf-8 -*-

import typing as T

from ..config.api import Database, Schema
from ..sa.api import (
    SchemaInfo,
)

if T.TYPE_CHECKING:  # pragma: no cover
    from .hub import Hub


class SaHubMixin:
    def get_database_and_schema_object(
        self: "Hub",
        database_identifier: str,
        schema_name: T.Optional[str] = None,
    ) -> tuple[
        bool,
        str,
        T.Optional["Database"],
        T.Optional["Schema"],
    ]:
        """
        Retrieves the database and schema objects based on the provided identifiers.

        :param database_identifier: The identifier of the database to query.
        :param schema_name: Optional schema name to filter the results. If not provided,

        :returns: A tuple containing:
            - A boolean indicating success or failure.
            - An error message if applicable.
            - The Database object if found, otherwise None.
            - The Schema object if found, otherwise None.
        """
        if database_identifier not in self.config.databases_mapping:
            return (
                False,
                f"Error: Database '{database_identifier}' not found in configuration.",
                None,
                None,
            )
        database = self.config.databases_mapping[database_identifier]
        if schema_name not in database.schemas_mapping:
            return (
                False,
                f"Error: Schema '{schema_name}' not found in '{database_identifier}' database.",
                None,
                None,
            )
        schema = database.schemas_mapping[schema_name]
        return True, "", database, schema

    def get_schema_info(
        self: "Hub",
        database: "Database",
        schema: "Schema",
    ) -> SchemaInfo:
        """
        Retrieves the schema information for a specific database and schema.

        :param database: The database object containing the SQLAlchemy engine and metadata.
        :param schema: The schema object containing the name and table filters.
        :returns: A SchemaInfo object containing the schema details.
        """
        return SchemaInfo.from_metadata(
            engine=database.sa_engine,
            metadata=database.sa_metadata,
            schema_name=schema.name,
            include=schema.table_filter.include,
            exclude=schema.table_filter.exclude,
        )
