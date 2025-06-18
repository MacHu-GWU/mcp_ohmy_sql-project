# -*- coding: utf-8 -*-

import typing as T
import itertools

import sqlalchemy as sa
import redshift_connector
from s3pathlib import S3Path
import polars_writer.api as pw
import aws_sdk_polars.api as aws_pl

from ..logger import logger
from ..aws.aws_redshift.api import Session

from .chinook.chinook_data_model import (
    Base,
)
from .chinook.chinook_data_loader import chinook_data_loader
from .aws.constants import redshift_iam_role_name
from .aws.s3_enum import bsm, s3dir_tests_aws_redshift_staging
from .aws.aws_redshift_model import (
    sql_create_table_mappings,
    sql_drop_table_mappings,
)

if T.TYPE_CHECKING:  # pragma: no cover
    import polars as pl

try:
    from rich import print as rprint
except ImportError:  # pragma: no cover
    pass


@logger.emoji_block(
    msg="Drop all Redshift tables",
    emoji="🗑",
)
def drop_all_redshift_tables(
    conn_or_engine: T.Union[
        redshift_connector.Connection,
        sa.Engine,
    ],
):
    if isinstance(conn_or_engine, redshift_connector.Connection):
        with Session(conn_or_engine) as cursor:
            for sql in sql_drop_table_mappings.values():
                cursor.execute(sql)
            conn_or_engine.commit()
    elif isinstance(conn_or_engine, sa.Engine):
        with conn_or_engine.connect() as conn:
            for sql in sql_drop_table_mappings.values():
                conn.execute(sa.text(sql))
            conn.commit()
    else:  # pragma: no cover
        raise TypeError
    logger.info("Done")


@logger.emoji_block(
    msg="Create all Redshift tables",
    emoji="🆕",
)
def create_all_redshift_tables(
    conn_or_engine: T.Union[
        redshift_connector.Connection,
        sa.Engine,
    ],
):
    if isinstance(conn_or_engine, redshift_connector.Connection):
        with Session(conn_or_engine) as cursor:
            for sql in sql_create_table_mappings.values():
                cursor.execute(sql)
            conn_or_engine.commit()
    elif isinstance(conn_or_engine, sa.Engine):
        with conn_or_engine.connect() as conn:
            for sql in sql_create_table_mappings.values():
                conn.execute(sa.text(sql))
            conn.commit()
    else:  # pragma: no cover
        raise TypeError
    logger.info("Done")


polars_parquet_writer = pw.Writer(
    format="parquet",
    parquet_compression="snappy",
)


def _copy_from_s3(
    cursor: "redshift_connector.Cursor",
    table_name: str,
    df: "pl.DataFrame",
    s3_uri: str,
    role_arn: str,
):
    """
    takes 23.5 seconds to insert all data.
    """
    aws_pl.s3.write(
        df,
        s3_client=bsm.s3_client,
        s3path=S3Path(s3_uri),
        polars_writer=polars_parquet_writer,
    )
    sql = f"""
COPY {table_name}
FROM '{s3_uri}'
iam_role '{role_arn}'
PARQUET
;
""".strip()
    # print(sql) # for debugging only
    cursor.execute(sql)


def _insert_many(
    cursor: "redshift_connector.Cursor",
    table: "sa.Table",
    df: "pl.DataFrame",
):
    """
    takes 21.0 seconds to insert all data.
    """
    columns = []
    values = []
    for col_name in table.columns.keys():
        columns.append(col_name)
        values.append("%s")
    columns_def = ", ".join(columns)
    values_def = ", ".join(values)
    values_def_1 = f"({values_def})"
    values_def_2 = [values_def_1] * df.shape[0]
    values_def_3 = ", ".join(values_def_2)
    sql = f"INSERT INTO {table.name} ({columns_def}) VALUES {values_def_3};"
    rows = df.rows()
    flat_rows = list(itertools.chain.from_iterable(rows))
    # logger.info(sql)  # for debugging only
    # rprint(flat_rows)  # for debugging only
    cursor.execute(sql, flat_rows)
    # conn.commit()


@logger.emoji_block(
    msg="Insert data into {table.name!r} Table",
    emoji="📥",
)
def insert_data_to_one_table(
    cursor: "redshift_connector.Cursor",
    table: "sa.Table",
):
    table_name = table.name
    df = chinook_data_loader.get_table_df(table.name)
    # print(df) # for debugging only
    logger.info(f"{df.shape = }")  # for debugging only

    def copy_from_s3():
        s3path = s3dir_tests_aws_redshift_staging / f"{table_name}.parquet"
        # print(s3path.console_url) # for debugging only
        role_arn = f"arn:aws:iam::{bsm.aws_account_id}:role/{redshift_iam_role_name}"
        _copy_from_s3(cursor, table_name, df, s3path, role_arn)

    def insert_many():
        _insert_many(cursor, table, df)

    with logger.nested():
        # copy_from_s3()
        insert_many()


@logger.emoji_block(
    msg="Insert all data to Redshift",
    emoji="📥",
)
def insert_all_data_to_redshift(
    conn: redshift_connector.Connection,
):
    with Session(conn) as cursor:
        for table in list(Base.metadata.sorted_tables):
            with logger.nested():
                insert_data_to_one_table(
                    cursor=cursor,
                    table=table,
                )
            conn.commit()
            # break
    logger.info("Done")
