# -*- coding: utf-8 -*-

"""
Relational database adapter mixin for SQLAlchemy-based database operations.
"""

import typing as T

from ..constants import DbTypeEnum
from ..config.api import Database, Schema
from ..db.relational import api as relational

if T.TYPE_CHECKING:  # pragma: no cover
    from .adapter import Adapter


class RelationalAdapterMixin:
    """
    Adapter mixin for relational database operations using SQLAlchemy and the db/relational module.
    """
    def get_relational_schema_info(
        self: "Adapter",
        database: "Database",
        schema: "Schema",
    ) -> relational.SchemaInfo:
        """
        Retrieves the schema information for a specific database and schema.

        :param database: The database object that contains the SQLAlchemy engine and metadata.
        :param schema: The schema object containing the name and table filters.

        :returns: A SchemaInfo object containing the schema details.
        """
        schema_info = relational.new_schema_info(
            engine=database.connection.sa_engine,
            metadata=database.sa_metadata,
            schema_name=schema.name,
            include=schema.table_filter.include,
            exclude=schema.table_filter.exclude,
        )
        return schema_info

    def get_relational_database_info(
        self: "Adapter",
        database: "Database",
    ) -> relational.DatabaseInfo:
        """
        Retrieves the database information for a specific database.

        :param database: The database object that contains the SQLAlchemy engine and metadata.

        :returns: A DatabaseInfo object containing the all schema details.
        """
        schemas = list()
        for schema in database.schemas:
            schema_info = self.get_relational_schema_info(database, schema)
            schemas.append(schema_info)
        database_info = relational.new_database_info(
            name=database.identifier,
            db_type=DbTypeEnum.get_by_value(database.db_type),
            schemas=schemas,
            comment=database.description,
        )
        return database_info
