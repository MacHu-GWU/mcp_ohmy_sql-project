# -*- coding: utf-8 -*-

from mcp_ohmy_sql.db.relational import (
    ForeignKeyInfo,
    ColumnInfo,
    TableInfo,
    SchemaInfo,
    DatabaseInfo,
)


def test():
    _ = ForeignKeyInfo
    _ = ColumnInfo
    _ = TableInfo
    _ = SchemaInfo
    _ = DatabaseInfo


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.db.relational",
        preview=False,
    )
