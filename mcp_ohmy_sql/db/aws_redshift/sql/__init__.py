# -*- coding: utf-8 -*-

from functools import cached_property
from pathlib import Path

dir_here = Path(__file__).absolute().parent


def load_sql(name: str) -> str:
    path = dir_here / f"{name}.sql"
    return path.read_text(encoding="utf-8").strip()


class _SqlEnum:
    @cached_property
    def schema_info_sql(self) -> str:
        return load_sql("schema_info")

    @cached_property
    def table_info_sql(self) -> str:
        return load_sql("table_info")

    @cached_property
    def column_info_sql(self) -> str:
        return load_sql("column_info")


SqlEnum = _SqlEnum()
