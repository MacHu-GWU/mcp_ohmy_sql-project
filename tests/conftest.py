# -*- coding: utf-8 -*-

import typing as T
import dataclasses

import pytest
import sqlalchemy as sa

from mcp_ohmy_sql.constants import ObjectTypeEnum, DbTypeEnum
from mcp_ohmy_sql.sa.utils import get_create_view_sql
from mcp_ohmy_sql.db.relational.schema_model import (
    ForeignKeyInfo,
    ColumnInfo,
    TableInfo,
    SchemaInfo,
    DatabaseInfo,
)
from mcp_ohmy_sql.db.relational.schema_extractor import (
    new_foreign_key_info,
    new_column_info,
    new_table_info,
    new_schema_info,
    new_database_info,
)
from mcp_ohmy_sql.tests.chinook.chinook_data_model import (
    Base,
    VIEW_NAME_AND_SELECT_STMT_MAP,
    ChinookTableNameEnum,
    ChinookViewNameEnum,
    Artist,
    Album,
    album_sales_stats_view_select_stmt,
)


@dataclasses.dataclass
class SaEngineObjs:
    engine: sa.Engine
    metadata: sa.MetaData


@pytest.fixture(scope="function")
def in_memory_sqlite_engine_objs() -> T.Generator[SaEngineObjs, None, None]:
    """
    Fixture to create an in-memory SQLite database engine for testing.

    This fixture sets up a new SQLite database in memory, creates the necessary tables,
    and returns the engine. The database is reset after each test function.
    """
    engine = sa.create_engine("sqlite:///:memory:")

    # create tables
    Base.metadata.create_all(engine)

    # create views
    with engine.connect() as conn:
        for view_name, select_stmt in VIEW_NAME_AND_SELECT_STMT_MAP.items():
            create_view_sql = get_create_view_sql(
                engine=engine,
                view_name=view_name,
                select=select_stmt,
                db_type=DbTypeEnum.SQLITE,
            )
            conn.execute(sa.text(create_view_sql))
        conn.commit()

    # get the latest metadata with views
    metadata = sa.MetaData()
    metadata.reflect(engine, views=True)

    yield SaEngineObjs(
        engine=engine,
        metadata=metadata,
    )

    # drop views
    with engine.connect() as conn:
        view_name_list = list(VIEW_NAME_AND_SELECT_STMT_MAP)
        view_name_list = view_name_list[::-1]  # reverse order to drop views first
        for view_name in view_name_list:
            sql = f'DROP VIEW IF EXISTS "{view_name}"'
            stmt = sa.text(sql)
            conn.execute(stmt)
        conn.commit()

    # drop tables
    Base.metadata.drop_all(engine)  # this method doesn't drop views

    # clear metadata
    metadata.clear()


@dataclasses.dataclass
class SAObjs:
    t_album: sa.Table
    c_album_album_id: sa.Column
    c_album_title_id: sa.Column
    c_album_artist_id: sa.Column
    fk_album_artist_id: sa.ForeignKey
    t_album_sales_stats: sa.Table


@pytest.fixture(scope="function")
def in_memory_sqlite_sa_objects(
    in_memory_sqlite_engine_objs,
) -> SAObjs:
    metadata = in_memory_sqlite_engine_objs.metadata

    t_album = metadata.tables[ChinookTableNameEnum.Album.value]

    c_album_album_id = t_album.columns[Album.AlbumId.name]
    c_album_title_id = t_album.columns[Album.Title.name]
    c_album_artist_id = t_album.columns[Album.ArtistId.name]

    fk_album_artist_id = list(c_album_artist_id.foreign_keys)[0]

    t_album_sales_stats = metadata.tables[ChinookViewNameEnum.AlbumSalesStats.value]

    return SAObjs(
        t_album=t_album,
        c_album_album_id=c_album_album_id,
        c_album_title_id=c_album_title_id,
        c_album_artist_id=c_album_artist_id,
        fk_album_artist_id=fk_album_artist_id,
        t_album_sales_stats=t_album_sales_stats,
    )


@dataclasses.dataclass
class SchemaInfoObjs:
    fk_album_artist_id_info: ForeignKeyInfo
    c_album_album_id_info: ColumnInfo
    c_album_title_id_info: ColumnInfo
    c_album_artist_id_info: ColumnInfo
    t_album_info: TableInfo
    v_album_sales_stats_info: TableInfo
    schema_info: SchemaInfo
    database_info: DatabaseInfo


@pytest.fixture(scope="function")
def in_memory_sqlite_sa_schema_info_objects(
    in_memory_sqlite_engine_objs,
    in_memory_sqlite_sa_objects,
) -> SchemaInfoObjs:
    engine = in_memory_sqlite_engine_objs.engine
    metadata = in_memory_sqlite_engine_objs.metadata
    sa_objs = in_memory_sqlite_sa_objects

    fk_album_artist_id_info = new_foreign_key_info(sa_objs.fk_album_artist_id)

    c_album_album_id_info = new_column_info(
        table=sa_objs.t_album,
        column=sa_objs.c_album_album_id,
    )
    c_album_title_id_info = new_column_info(
        table=sa_objs.t_album,
        column=sa_objs.c_album_title_id,
    )
    c_album_artist_id_info = new_column_info(
        table=sa_objs.t_album,
        column=sa_objs.c_album_artist_id,
    )
    t_album_info = new_table_info(
        table=sa_objs.t_album,
        object_type=ObjectTypeEnum.TABLE,
    )
    v_album_sales_stats_info = new_table_info(
        table=sa_objs.t_album_sales_stats,
        object_type=ObjectTypeEnum.VIEW,
    )

    schema_info = new_schema_info(
        engine=engine,
        metadata=metadata,
        schema_name=None,
        exclude=["PlaylistTrack", "Playlist"],
    )
    database_info = new_database_info(
        name="Chinook",
        db_type=DbTypeEnum.SQLITE,
        schemas=[schema_info],
    )

    schema_info_objs = SchemaInfoObjs(
        fk_album_artist_id_info=fk_album_artist_id_info,
        c_album_album_id_info=c_album_album_id_info,
        c_album_title_id_info=c_album_title_id_info,
        c_album_artist_id_info=c_album_artist_id_info,
        t_album_info=t_album_info,
        v_album_sales_stats_info=v_album_sales_stats_info,
        schema_info=schema_info,
        database_info=database_info,
    )

    return schema_info_objs
