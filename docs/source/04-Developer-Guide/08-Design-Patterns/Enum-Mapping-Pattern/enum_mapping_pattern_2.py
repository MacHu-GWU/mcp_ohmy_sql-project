# -*- coding: utf-8 -*-

"""
Enum Mapping Pattern Example 2 (Not recommended)
"""

import enum
import typing as T
import dataclasses
from enum_mate.api import EnumMixin


@dataclasses.dataclass
class DbObject:
    type: str = dataclasses.field()
    table_type: T.Optional[str] = dataclasses.field()

    def __hash__(self):
        return hash(self.type)


class DbObjectTypeEnum(EnumMixin, enum.Enum):
    # fmt: off
    database = DbObject(type="database", table_type=None)
    table = DbObject(type="table", table_type="Table")
    view = DbObject(type="view", table_type="View")
    materialized_view = DbObject(type="materialized_view", table_type="MaterializedView")
    # fmt: on


if __name__ == "__main__":
    print(f"{DbObjectTypeEnum.table.value = }")
    print(f"{DbObjectTypeEnum.table.value.table_type = }")
