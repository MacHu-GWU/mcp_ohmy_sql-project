# -*- coding: utf-8 -*-

from mcp_ohmy_sql.utils import dedent
from mcp_ohmy_sql.constants import (
    DbTypeEnum,
    LLMTypeEnum,
    ObjectTypeEnum,
)
from mcp_ohmy_sql.db.aws_redshift.schema_1_model import (
    ColumnInfo,
    TableInfo,
    SchemaInfo,
    DatabaseInfo,
)
from mcp_ohmy_sql.db.aws_redshift.schema_2_encoder import (
    encode_column_info,
    encode_table_info,
    encode_schema_info,
    encode_database_info,
)

column_info_1 = ColumnInfo(
    name="user_id",
    type="str",
    llm_type=LLMTypeEnum.STR,
    dist_key=True,
    sort_key_position=0,
    encoding="lzo",
    notnull=True,
)
column_info_2 = ColumnInfo(
    name="create_time",
    type="timestamp",
    llm_type=LLMTypeEnum.DT,
    dist_key=False,
    sort_key_position=1,
    encoding="delta",
    notnull=True,
)
column_info_3 = ColumnInfo(
    name="description",
    type="str",
    llm_type=LLMTypeEnum.STR,
    dist_key=False,
    sort_key_position=0,
    encoding="lzo",
    notnull=False,
)

table_info_1 = TableInfo(
    object_type=ObjectTypeEnum.TABLE,
    name="users",
    dist_style="KEY",
    owner="admin",
    columns=[
        column_info_1,
    ],
)

schema_info_1 = SchemaInfo(
    name="public",
    tables=[
        table_info_1,
    ],
)

database_info_1 = DatabaseInfo(
    name="mcp_ohmy_sql_dev",
    db_type=DbTypeEnum.AWS_REDSHIFT,
    schemas=[
        schema_info_1,
    ],
)


def test_encode_column_info():
    s = encode_column_info(column_info_1)
    expected = "user_id:str*DK*NN*lzo"
    assert s == expected

    s = encode_column_info(column_info_2)
    expected = "create_time:dt*SK-1*NN*delta"
    assert s == expected

    s = encode_column_info(column_info_3)
    expected = "description:str*lzo"
    assert s == expected


def test_encode_table_info():
    s = encode_table_info(table_info_1)
    # print(s)  # for debugging only
    expected = dedent(
        """
    Table users KEY Distribution Style (
        user_id:str*DK*NN*lzo,
    )
    """
    )
    assert s == expected


def test_encode_schema_info():
    s = encode_schema_info(schema_info=schema_info_1)
    # print(s)  # for debugging only
    expected = dedent(
        """
    Schema public (
        Table users KEY Distribution Style (
            user_id:str*DK*NN*lzo,
        ),
    )
    """
    )
    assert s == expected


def test_encode_database_info():
    s = encode_database_info(database_info=database_info_1)
    # print(s)  # for debugging only
    expected = dedent(
        """
        aws_redshift Database mcp_ohmy_sql_dev (
            Schema public (
                Table users KEY Distribution Style (
                    user_id:str*DK*NN*lzo,
                ),
            ),
        )
        """
    )
    assert s == expected


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.db.aws_redshift.schema_3_encoder",
        preview=False,
    )
