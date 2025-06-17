# -*- coding: utf-8 -*-

"""
Enum Mapping Pattern Example

This module demonstrates best practices for creating mappings between multiple enums.
We explore a scenario where we have two enums with values that need to be mapped to each other.

Example Use Case:
We have a DatabaseObject enum and a TableType enum. DatabaseObject represents database entities
(schemas, databases, tables, views) with descriptive names, while TableType has encoded names
suitable for programming contexts (e.g., "materialized view" becomes "MaterializedView" to
avoid spaces in identifiers).

Two Approaches Considered:

1. Dictionary Mapping with Property Access (Implemented):
   - Define separate enums for DatabaseObject and TableType
   - Create a dictionary mapping between them
   - Add a property to the enum class for convenient access
   - Benefits: Easy to use, no need to import mapping dictionary or TableType enum
   - Usage: database_obj.table_type instead of mapping[database_obj]

2. Tuple-based DataClass (Not Implemented):
   - Define a single dataclass containing both enum values as fields
   - Benefits: Guaranteed consistency between related values
   - Drawbacks: Less flexible, can't iterate over individual enum types separately
   - Not suitable for cases where not all values have mappings (e.g., database has no TableType)

This example focuses on approach #1 as it provides better flexibility and ease of use
for our specific requirements.
"""

from enum_mate.api import BetterStrEnum


class DbObjectTypeEnum(BetterStrEnum):
    database = "database"
    table = "table"
    view = "view"
    materialized_view = "materialized view"

    @property
    def table_type(self) -> "TableTypeEnum":
        return db_obj_type_to_table_type_mapping[self]


class TableTypeEnum(BetterStrEnum):
    Table = "Table"
    View = "View"
    MaterializedView = "MaterializedView"


db_obj_type_to_table_type_mapping = {
    DbObjectTypeEnum.table: TableTypeEnum.Table,
    DbObjectTypeEnum.view: TableTypeEnum.View,
    DbObjectTypeEnum.materialized_view: TableTypeEnum.MaterializedView,
}

if __name__ == "__main__":
    print(f"{DbObjectTypeEnum.table.table_type.value = }")
    print(f"{DbObjectTypeEnum.database.table_type.value = }")
