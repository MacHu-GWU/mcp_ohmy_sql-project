# -*- coding: utf-8 -*-

import typing as T
import json
import textwrap
from pathlib import Path
from functools import cached_property

from pydantic import BaseModel, Field

from ..sa.api import (
    SchemaInfo,
    encode_schema_info,
)

if T.TYPE_CHECKING:  # pragma: no cover
    from .config_define_00_main import Config


class ConfigDatabaseSchemaMixin:
    def get_database_schema(self: "Config") -> str:
        for database in self.databases:
            lines = []
            for schema in database.schemas:
                schema_info = SchemaInfo.from_metadata(
                    engine=database.sa_engine,
                    metadata=database.sa_metadata,
                    schema_name=schema.name,
                )
                s = encode_schema_info(schema_info)
                # lines.append(textwrap.indent())