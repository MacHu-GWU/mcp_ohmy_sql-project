SELECT
    td.schemaname AS schema_name,
    td.tablename AS table_name,
    td.column AS column_name,
    td.type AS column_type,
    td.encoding AS column_encoding,
    td.distkey AS is_column_a_distkey,
    td.sortkey AS sortkey_position,
    td.notnull AS is_column_notnull
FROM pg_table_def td
WHERE td.schemaname NOT IN ('pg_catalog', 'information_schema')
;