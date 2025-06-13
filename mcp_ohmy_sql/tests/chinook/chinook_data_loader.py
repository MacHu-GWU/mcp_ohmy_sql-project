# -*- coding: utf-8 -*-

import json
from functools import cached_property

import polars as pl
import sqlalchemy as sa
from pydantic import BaseModel, Field

from .chinook_data_file import path_ChinookData_json
from .chinook_data_model import (
    Base,
    ChinookTableNameEnum,
    ChinookViewNameEnum,
    Artist,
    Album,
    Genre,
    MediaType,
    Track,
    Playlist,
    PlaylistTrack,
    Employee,
    Customer,
    Invoice,
    InvoiceLine,
)


class ChinookDataLoader:
    @cached_property
    def data(self) -> dict:
        """
        Raw data from the Chinook dataset.
        """
        return json.loads(path_ChinookData_json.read_text(encoding="utf-8"))

    @cached_property
    def table_name_list(self) -> list[str]:
        """
        List of table names in the Chinook dataset.
        """
        return list(self.data.keys())

    def get_table_df(self, table_name: str) -> pl.DataFrame:
        """
        Get rows from a specific table in the Chinook dataset.

        :param table_name: Name of the table to retrieve data from.

        :return: DataFrame containing the rows of the specified table.
        """

        table = Base.metadata.tables[table_name]
        df = pl.DataFrame(self.data[table_name])

        # process datatime columns
        for col_name, col in table.columns.items():
            if isinstance(col.type, sa.Integer):
                df = df.with_columns(
                    **{
                        col_name: pl.col(col_name).cast(pl.Int32),
                    }
                )
            if isinstance(col.type, sa.DateTime):
                df = df.with_columns(
                    **{
                        col_name: pl.col(col_name).str.strptime(
                            pl.Datetime, format="%Y-%m-%dT%H:%M:%S"
                        ),
                    }
                )
            if isinstance(col.type, sa.DECIMAL):
                df = df.with_columns(
                    **{
                        col_name: pl.col(col_name).cast(
                            pl.Decimal(precision=10, scale=2)
                        ),
                    }
                )
        return df


chinook_data_loader = ChinookDataLoader()
