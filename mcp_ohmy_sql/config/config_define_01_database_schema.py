# -*- coding: utf-8 -*-

import typing as T
import json
import textwrap
from pathlib import Path
from functools import cached_property

from pydantic import BaseModel, Field
from ..constants import TAB
from ..sa.api import (
    SchemaInfo,
    encode_schema_info,
)

if T.TYPE_CHECKING:  # pragma: no cover
    from .config_define_00_main import Config


class ConfigDatabaseSchemaMixin:
    def get_database_schema(self: "Config") -> str:
        """
        Generates and returns the schema definition strings for all databases,
        all schemas, all tables associated with the Config object,
        formatted into a structured representation.

        :returns: A formatted string representation of the schema definitions for all
            databases.
        """
        database_lines = []
        for database in self.databases:
            schema_lines = []
            for schema in database.schemas:
                schema_info = SchemaInfo.from_metadata(
                    engine=database.sa_engine,
                    metadata=database.sa_metadata,
                    schema_name=schema.name,
                )
                s = encode_schema_info(schema_info)
                schema_lines.append(textwrap.indent(s, prefix=TAB))
            schemas_def = "\n".join(schema_lines)
            s = f"Database {database.identifier}(\n{schemas_def}\n)"
            database_lines.append(s)
        databases_def = "\n".join(database_lines)
        return databases_def
