# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy.types import TypeEngine
from mcp_ohmy_sql.db.aws_redshift.schema_1_model import (
    ColumnInfo,
    TableInfo,
    SchemaInfo,
    DatabaseInfo,
)
from mcp_ohmy_sql.db.aws_redshift.schema_3_extractor import (
    SqlEnum,
)
from mcp_ohmy_sql.constants import ObjectTypeEnum, LLMTypeEnum, DbTypeEnum

# from mcp_ohmy_sql.db.relational.schema_2_extractor import (
#     sqlalchemy_type_to_llm_type,
#     new_foreign_key_info,
#     new_column_info,
#     new_table_info,
#     new_schema_info,
#     new_database_info,
# )
#
# from mcp_ohmy_sql.tests.chinook.chinook_data_model import (
#     ChinookTableNameEnum,
#     ChinookViewNameEnum,
#     Artist,
# )


def test_new_column_info(
    rs_conn,
):

    cursor = rs_conn.cursor()

    column_rows = cursor.execute(SqlEnum.column_info_sql).fetchall()
    column_tuple_mapping: dict[str, dict[str, list[tuple]]] = {}
    for row in column_rows:
        schema_name = row[0]
        column_tuple_mapping.setdefault(schema_name, {})
        table_name = row[1]
        try:
            column_tuple_mapping[schema_name][table_name].append(row)
        except KeyError:
            column_tuple_mapping[schema_name][table_name] = [row]

    table_rows = cursor.execute(SqlEnum.table_info_sql).fetchall()
    table_tuple_mapping: dict[str, list[tuple]] = {}
    for row in table_rows:
        schema_name = row[0]
        try:
            table_tuple_mapping[schema_name].append(row)
        except KeyError:
            table_tuple_mapping[schema_name] = [row]

    schema_rows = cursor.execute(SqlEnum.schema_info_sql).fetchall()
    schemas = list()
    for row in schema_rows:
        schema_name, schema_description = row[0], row[1]
        tables = list()
        for table_row in table_tuple_mapping.get(schema_name, []):
            table_name = table_row[1]
            columns = list()
            for column_row in column_tuple_mapping.get(schema_name, {}).get(table_name, []):
                column_info = ColumnInfo(
                    name=column_row[2],
                    type=column_row[3],
                    llm_type=column_row[3],
                    dist_key=column_row[5],
                    sort_key_position=column_row[6],
                    encoding=column_row[4],
                    notnull=column_row[7],
                )
                columns.append(column_info)
            table_info = TableInfo(
                object_type=ObjectTypeEnum.TABLE,
                name=table_name,
                dist_style=table_row[2],
                owner=table_row[3],
                columns=columns,
            )
            tables.append(table_info)
        schema_info = SchemaInfo(
            name=schema_name,
            comment=schema_description,
            tables=tables,
        )
        schemas.append(schema_info)

    database_info = DatabaseInfo(
        name="Redshift",
        schemas=schemas,
    )
    from rich import print as rprint
    rprint(database_info)
    cursor.close()


#     sa_objs = in_memory_sqlite_sa_objects
#
#     c_album_album_id_info = new_column_info(
#         table=sa_objs.t_album,
#         column=sa_objs.c_album_album_id,
#     )
#     assert c_album_album_id_info.llm_type is LLMTypeEnum.INT
#     assert c_album_album_id_info.primary_key is True
#     assert c_album_album_id_info.nullable is False
#
#     c_album_title_id_info = new_column_info(
#         table=sa_objs.t_album,
#         column=sa_objs.c_album_title_id,
#     )
#     assert c_album_title_id_info.llm_type is LLMTypeEnum.STR
#     assert c_album_title_id_info.primary_key is False
#     assert c_album_title_id_info.nullable is False
#
#     c_album_artist_id_info = new_column_info(
#         table=sa_objs.t_album,
#         column=sa_objs.c_album_artist_id,
#     )
#     assert c_album_artist_id_info.object_type is ObjectTypeEnum.COLUMN
#     assert c_album_artist_id_info.llm_type is LLMTypeEnum.INT
#     assert c_album_artist_id_info.primary_key is False
#     assert c_album_artist_id_info.nullable is False
#
#
# def test_new_table_info(
#     in_memory_sqlite_sa_objects,
# ):
#     sa_objs = in_memory_sqlite_sa_objects
#
#     t_album_info = new_table_info(
#         table=sa_objs.t_album,
#         object_type=ObjectTypeEnum.TABLE,
#     )
#     assert t_album_info.object_type is ObjectTypeEnum.TABLE
#     assert t_album_info.name == ChinookTableNameEnum.Album.value
#     assert t_album_info.fullname == ChinookTableNameEnum.Album.value
#     assert len(t_album_info.primary_key) == 1
#     assert len(t_album_info.foreign_keys) == 1
#     assert len(t_album_info.columns) == 3
#
#
# def _test_new_schema_info_and_new_database_info(
#     engine: sa.engine.Engine,
#     metadata: sa.MetaData,
# ):
#     schema_info = new_schema_info(
#         engine=engine,
#         metadata=metadata,
#         schema_name=None,
#         exclude=["PlaylistTrack", "Playlist"],
#     )
#     assert schema_info.object_type is ObjectTypeEnum.SCHEMA
#     view = schema_info.tables_mapping[ChinookViewNameEnum.AlbumSalesStats.value]
#     assert view.object_type is ObjectTypeEnum.VIEW
#
#     database_info = new_database_info(
#         name="Chinook",
#         db_type=DbTypeEnum.SQLITE,
#         schemas=[schema_info],
#     )
#     assert database_info.object_type is ObjectTypeEnum.DATABASE
#
#
# def test_new_schema_info_and_new_database_info_1st(
#     in_memory_sqlite_engine_objs,
# ):
#     _test_new_schema_info_and_new_database_info(
#         in_memory_sqlite_engine_objs.engine,
#         in_memory_sqlite_engine_objs.metadata,
#     )
#
#
# def test_new_schema_info_and_new_database_info_2nd(
#     in_memory_sqlite_engine_objs,
# ):
#     _test_new_schema_info_and_new_database_info(
#         in_memory_sqlite_engine_objs.engine,
#         in_memory_sqlite_engine_objs.metadata,
#     )


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.db.aws_redshift.schema_2_extractor.py",
        preview=False,
    )
