# -*- coding: utf-8 -*-

import typing as T
import json
from pathlib import Path
from functools import cached_property

import sqlalchemy as sa
from pydantic import BaseModel, Field





# class TableFilterConfiguration(BaseModel):
#     include: path


class Config(BaseModel):
    version: str = Field()
    db_url: str = Field()
    db_schema: T.Optional[str] = Field(default=None)

    @classmethod
    def load(cls, path: Path):
        return cls(**json.loads(path.read_text()))

    @cached_property
    def engine(self) -> sa.Engine:
        return sa.create_engine(self.db_url)

    @cached_property
    def metadata(self) -> sa.MetaData:
        metadata = sa.MetaData()
        metadata.reflect(self.engine, schema=self.db_schema)
        return metadata
