# -*- coding: utf-8 -*-

import typing as T
import textwrap

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
