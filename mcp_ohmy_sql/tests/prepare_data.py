# -*- coding: utf-8 -*-

import json
from functools import cached_property

import sqlalchemy as sa
import sqlalchemy.orm as orm
from .chinook import dir_tmp, path_ChinookData_json


class Base(orm.DeclarativeBase):
    """
    Ref: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
    """


class Artist(Base):
    __tablename__ = "Artist"

    ArtistId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Name: orm.Mapped[int] = sa.Column(sa.String, nullable=False)


class Album(Base):
    __tablename__ = "Album"

    AlbumId: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    Title: orm.Mapped[str] = sa.Column(sa.String, nullable=False)
    ArtistId: orm.Mapped[int] = sa.Column(sa.ForeignKey("Artist.ArtistId"))


class _EngineEnum:
    @cached_property
    def sqlite(self) -> sa.engine.Engine:
        path = dir_tmp / "Chinook_Sqlite.sqlite"
        return sa.create_engine(f"sqlite:///{path}")

    @cached_property
    def postgres(self) -> sa.engine.Engine:
        return sa.create_engine(
            "postgresql+psycopg2://postgres:password@localhost:40311/postgres"
        )


EngineEnum = _EngineEnum()


def prepare_data(engine: sa.engine.Engine):
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine, checkfirst=True)

    data = json.loads(path_ChinookData_json.read_text())
    with engine.connect() as conn:
        for table in Base.metadata.sorted_tables:
            rows = data[table.name]
            stmt = sa.insert(table)
            conn.execute(stmt, rows)
        conn.commit()
