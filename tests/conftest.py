# -*- coding: utf-8 -*-

import typing as T
import dataclasses

import pytest
import sqlalchemy as sa

from mcp_ohmy_sql.constants import ObjectTypeEnum, DbTypeEnum
from mcp_ohmy_sql.db.relational.schema_1_model import (
    ForeignKeyInfo,
    ColumnInfo,
    TableInfo,
    SchemaInfo,
    DatabaseInfo,
)
from mcp_ohmy_sql.db.relational.schema_2_extractor import (
    new_foreign_key_info,
    new_column_info,
    new_table_info,
    new_schema_info,
    new_database_info,
)
from mcp_ohmy_sql.config.config_define import Database, SqlalchemyConnection
from mcp_ohmy_sql.tests.chinook.chinook_data_model import (
    Base,
    ChinookTableNameEnum,
    ChinookViewNameEnum,
    VIEW_NAME_AND_SELECT_STMT_MAP,
    Album,
)
from mcp_ohmy_sql.tests.setup_relational_database import (
    drop_all_tables,
    create_all_tables,
    insert_all_data,
    drop_all_views,
    create_all_views,
)
from mcp_ohmy_sql.tests.test_config_1_define import DatabaseEnum


@dataclasses.dataclass
class SaEngineObjs:
    engine: sa.Engine
    metadata: sa.MetaData
    db_type: DbTypeEnum


@dataclasses.dataclass
class SaSchemaObjs:
    t_album: sa.Table
    c_album_album_id: sa.Column
    c_album_title_id: sa.Column
    c_album_artist_id: sa.Column
    fk_album_artist_id: sa.ForeignKey
    t_album_sales_stats: sa.Table


@dataclasses.dataclass
class SaSchemaInfoObjs:
    fk_album_artist_id_info: ForeignKeyInfo
    c_album_album_id_info: ColumnInfo
    c_album_title_id_info: ColumnInfo
    c_album_artist_id_info: ColumnInfo
    t_album_info: TableInfo
    v_album_sales_stats_info: TableInfo
    schema_info: SchemaInfo
    database_info: DatabaseInfo


# ------------------------------------------------------------------------------
# In-memory SQLite database fixtures
# ------------------------------------------------------------------------------
@pytest.fixture(scope="function")
def in_memory_sqlite_engine_objs():
    """
    Fixture to create an in-memory SQLite database engine for testing.

    This fixture sets up a new SQLite database in memory, creates the necessary tables,
    and returns the engine. The database is reset after each test function.
    """
    engine = sa.create_engine("sqlite:///:memory:")

    # create tables and views
    create_all_tables(engine=engine, metadata=Base.metadata, drop_first=False)
    create_all_views(engine=engine, db_type=DbTypeEnum.SQLITE)

    # get the latest metadata with views
    metadata = sa.MetaData()
    metadata.reflect(engine, views=True)

    yield SaEngineObjs(
        engine=engine,
        metadata=metadata,
        db_type=DbTypeEnum.SQLITE,
    )

    # drop views and tables
    drop_all_views(engine=engine, db_type=DbTypeEnum.SQLITE)
    drop_all_tables(engine=engine, metadata=Base.metadata)
    # clear metadata
    metadata.clear()


@pytest.fixture(scope="function")
def in_memory_sqlite_sa_objects(
    in_memory_sqlite_engine_objs,
) -> SaSchemaObjs:
    metadata = in_memory_sqlite_engine_objs.metadata

    t_album = metadata.tables[ChinookTableNameEnum.Album.value]

    c_album_album_id = t_album.columns[Album.AlbumId.name]
    c_album_title_id = t_album.columns[Album.Title.name]
    c_album_artist_id = t_album.columns[Album.ArtistId.name]

    fk_album_artist_id = list(c_album_artist_id.foreign_keys)[0]

    t_album_sales_stats = metadata.tables[ChinookViewNameEnum.AlbumSalesStats.value]

    return SaSchemaObjs(
        t_album=t_album,
        c_album_album_id=c_album_album_id,
        c_album_title_id=c_album_title_id,
        c_album_artist_id=c_album_artist_id,
        fk_album_artist_id=fk_album_artist_id,
        t_album_sales_stats=t_album_sales_stats,
    )


@pytest.fixture(scope="function")
def in_memory_sqlite_sa_schema_info_objects(
    in_memory_sqlite_engine_objs,
    in_memory_sqlite_sa_objects,
) -> SaSchemaInfoObjs:
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
    schema_info_objs = SaSchemaInfoObjs(
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


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
@pytest.fixture(scope="class")
def sa_engine_factory():
    """ """
    created_sa_engine_objs_list: list[SaEngineObjs] = list()

    def _create_sa_engine_objs(
        engine: sa.Engine,
        db_type: DbTypeEnum,
    ) -> SaEngineObjs:
        # create tables and views
        create_all_tables(engine=engine, metadata=Base.metadata, drop_first=True)
        create_all_views(engine=engine, db_type=db_type)
        # insert all data
        insert_all_data(engine=engine, metadata=Base.metadata)

        # get the latest metadata with views
        metadata = sa.MetaData()
        metadata.reflect(engine, views=True)

        sa_engine_objs = SaEngineObjs(
            engine=engine,
            metadata=metadata,
            db_type=db_type,
        )
        created_sa_engine_objs_list.append(sa_engine_objs)
        return sa_engine_objs

    yield _create_sa_engine_objs

    for sa_engine_objs in created_sa_engine_objs_list:
        engine = sa_engine_objs.engine
        metadata = sa_engine_objs.metadata
        db_type = sa_engine_objs.db_type

        # drop views
        drop_all_views(engine=engine, db_type=db_type)
        drop_all_tables(engine=engine, metadata=Base.metadata)

        # clear metadata
        metadata.clear()


# @pytest.fixture(scope="class")
# def sa_data_factory(
#     sa_engine_factory,
# ):
#     def _create_sa(
#         engine: sa.Engine,
#         db_type: DbTypeEnum,
#     ):
#         sa_engine_objs = sa_engine_factory(engine=engine, db_type=db_type)
#
#
#     return _create_sa
