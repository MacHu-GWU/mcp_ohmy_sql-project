# -*- coding: utf-8 -*-
import textwrap

import polars_writer.api as pw
import aws_sdk_polars.api as aws_pl

from .chinook.chinook_data_model import Base
from .chinook.chinook_data_loader import chinook_data_loader
from .aws.constants import redshift_iam_role_name
from .aws.s3_enum import bsm, s3dir_tests_aws_redshift_staging
from .aws.redshift import (
    table_creation_scripts,
    table_drop_scripts,
)
from .test_config import DatabaseEnum


def setup_test_redshift_database():
    conn = DatabaseEnum.chinook_redshift.connection.conn
    cursor = conn.cursor()
    for table_name, sql_drop_table in table_drop_scripts.items():
        cursor.execute(sql_drop_table)
    for table_name, sql_create_table in table_creation_scripts.items():
        cursor.execute(sql_create_table)
    conn.commit()

    writer = pw.Writer(
        format="parquet",
        parquet_compression="snappy",
    )
    for table in Base.metadata.sorted_tables:
        table_name = table.name
        # print(f"----- {table_name} -----") # for debugging only
        s3path = s3dir_tests_aws_redshift_staging / f"{table_name}.parquet"
        # print(s3path.console_url) # for debugging only
        df = chinook_data_loader.get_table_df(table.name)
        # print(df) # for debugging only
        aws_pl.s3.write(
            df,
            s3_client=bsm.s3_client,
            s3path=s3path,
            polars_writer=writer,
        )
        sql = textwrap.dedent(
            f"""
        COPY {table_name}
        FROM '{s3path.uri}'
        iam_role 'arn:aws:iam::{bsm.aws_account_id}:role/{redshift_iam_role_name}'
        PARQUET
        ;
        """
        ).strip()
        # print(sql) # for debugging only
        cursor.execute(sql)
        conn.commit()

    conn.close()
