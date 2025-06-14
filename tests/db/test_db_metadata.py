# -*- coding: utf-8 -*-

from mcp_ohmy_sql.db.metadata import (
    ObjectTypeEnum,
    DbTypeEnum,
    BaseColumnInfo,
    BaseTableInfo,
    BaseSchemaInfo,
    BaseDatabaseInfo,
)


def test():
    table_info = BaseTableInfo(
        object_type=ObjectTypeEnum.TABLE,
        name="users",
        columns=[
            BaseColumnInfo(name="id"),
        ],
    )
    assert table_info.columns_mapping["id"] == table_info.columns[0]

    schema_info = BaseSchemaInfo(
        object_type=ObjectTypeEnum.SCHEMA,
        name="public",
        tables=[table_info],
    )
    assert schema_info.tables_mapping["users"] == schema_info.tables[0]

    db_info = BaseDatabaseInfo(
        object_type=ObjectTypeEnum.DATABASE,
        name="test_db",
        db_type=DbTypeEnum.POSTGRESQL,
        schemas=[schema_info],
    )
    assert db_info.schemas_mapping["public"] == db_info.schemas[0]


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.db.metadata",
        preview=False,
    )
