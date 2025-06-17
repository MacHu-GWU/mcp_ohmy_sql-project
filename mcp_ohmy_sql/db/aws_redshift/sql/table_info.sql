SELECT
    trim(pg_namespace.nspname) AS schema_name,
    trim(pg_class_info.relname) AS table_name,
    CASE WHEN pg_class_info.reldiststyle = 0 THEN 'EVEN'::text
        WHEN pg_class_info.reldiststyle = 1 THEN 'KEY'::text
        WHEN pg_class_info.reldiststyle = 8 THEN 'ALL'::text
        WHEN pg_class_info.releffectivediststyle = 10 THEN 'AUTO(ALL)'::text
        WHEN pg_class_info.releffectivediststyle = 11 THEN 'AUTO(EVEN)'::text
        WHEN pg_class_info.releffectivediststyle = 12 THEN 'AUTO(KEY)'::text ELSE '<<UNKNOWN>>'::text END AS diststyle,
    pg_user.usename AS owner_name,
    pg_description.description as description
FROM pg_class_info
LEFT JOIN pg_namespace
    ON pg_class_info.relnamespace = pg_namespace.oid
LEFT JOIN pg_description
    ON pg_namespace.oid = pg_description.objoid
LEFT JOIN pg_user
    ON pg_class_info.relowner = pg_user.usesysid
WHERE
    pg_namespace.nspname NOT IN ('information_schema', 'catalog_history')
    AND pg_namespace.nspname NOT LIKE 'pg_%'
;