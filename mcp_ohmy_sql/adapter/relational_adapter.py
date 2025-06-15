# -*- coding: utf-8 -*-

import typing as T

from ..config.api import Database, Schema
from ..db.relational import api as relational

if T.TYPE_CHECKING:  # pragma: no cover
    from .adapter import Adapter


class RelationalAdapterMixin:
    def get_relational_schema_info(
        self: "Adapter",
        database: "Database",
        schema: "Schema",
    ) -> relational.SchemaInfo:
        """
        Retrieves the schema information for a specific database and schema.

        :param database: The database object containing the SQLAlchemy engine and metadata.
        :param schema: The schema object containing the name and table filters.

        :returns: A SchemaInfo object containing the schema details.
        """
        schema_info = relational.new_schema_info(
            engine=database.sa_engine,
            metadata=database.sa_metadata,
            schema_name=schema.name,
            include=schema.table_filter.include,
            exclude=schema.table_filter.exclude,
        )
        return schema_info
