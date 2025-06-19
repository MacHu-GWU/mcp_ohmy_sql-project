# -*- coding: utf-8 -*-

"""

"""

import typing as T

from pydantic import BaseModel, Field

from ..config.api import Database, Schema, Config

from .relational_adapter import RelationalAdapterMixin
from .aws_redshift_adapter import AwsRedshiftAdapterMixin
from .tool_adapter import ToolAdapterMixin


class Adapter(
    BaseModel,
    RelationalAdapterMixin,
    AwsRedshiftAdapterMixin,
    ToolAdapterMixin,
):
    config: Config = Field()

    def get_database_and_schema_object(
        self: "Adapter",
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
            all_database = ", ".join(list(self.config.databases_mapping))
            return (
                False,
                (
                    f"Error: Database '{database_identifier}' not found in configuration. "
                    f"It has the following databases: {all_database}."
                ),
                None,
                None,
            )
        database = self.config.databases_mapping[database_identifier]
        if schema_name not in database.schemas_mapping:
            all_schema = ", ".join([name for name in database.schemas_mapping if name])
            return (
                False,
                (
                    f"Error: Schema '{schema_name}' not found in '{database_identifier}' database. "
                    f"It has the following schemas: {all_schema}."
                ),
                None,
                None,
            )
        schema = database.schemas_mapping[schema_name]
        return True, "", database, schema
