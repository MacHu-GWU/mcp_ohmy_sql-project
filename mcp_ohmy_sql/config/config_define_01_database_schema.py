# -*- coding: utf-8 -*-

import typing as T
import textwrap

from ..constants import TAB
from ..sa.api import (
    SchemaInfo,
    encode_schema_info,
)

if T.TYPE_CHECKING:  # pragma: no cover
    from .config_define_00_main import Config, Database, Schema


class ConfigDatabaseSchemaMixin:
    def get_schema_object(
        self: "Config",
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
        if database_identifier not in self.databases_mapping:
            return (
                False,
                f"Error: Database '{database_identifier}' not found in configuration.",
                None,
                None,
            )
        database = self.databases_mapping[database_identifier]
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
        self: "Config",
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

    def get_database_schema(self: "Config") -> str:
        """
        Generates and returns the schema definition strings for all databases,
        all schemas, all tables associated with the Config object,
        formatted into a structured representation.

        :returns: A structured text that includes all databases, schema, filtered tables,
            columns, relationships, and constraints in the following formats
            optimized for LLM consumption.

        Format::

            Database <Database 1 Identifier>(
              Schema <Schema 1 Name>(
                Table or View or MaterializedView <Table 1 Name>(
                  ${COLUMN_NAME}:${DATA_TYPE}${PRIMARY_KEY}${UNIQUE}${NOT_NULL}${INDEX}${FOREIGN_KEY},
                  more columns ...
                )
                more tables ...
              )
              more schemas ...
            )
            more databases ...

        There might be multiple Foreign Keys encoded as ``*FK->Table1.Column1*FK->Table2.Column2``.

        Constraints are encoded as:

        - *PK: Primary Key (implies unique and indexed)
        - *UQ: Unique constraint (implies indexed)
        - *NN: Not Null constraint
        - *IDX: Has database index
        - *FK->Table.Column: Foreign key reference
        """
        database_lines = []
        for database in self.databases:
            schema_lines = []
            for schema in database.schemas:
                schema_info = SchemaInfo.from_metadata(
                    engine=database.sa_engine,
                    metadata=database.sa_metadata,
                    schema_name=schema.name,
                    include=schema.table_filter.include,
                    exclude=schema.table_filter.exclude,
                )
                s = encode_schema_info(schema_info)
                schema_lines.append(textwrap.indent(s, prefix=TAB))
            schemas_def = "\n".join(schema_lines)
            s = f"Database {database.identifier}(\n{schemas_def}\n)"
            database_lines.append(s)
        databases_def = "\n".join(database_lines)
        return databases_def
