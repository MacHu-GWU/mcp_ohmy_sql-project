SELECT 
    pg_namespace.nspname as schema_name,
    pg_description.description as description
FROM pg_namespace
JOIN pg_description
    ON pg_namespace.oid = pg_description.objoid
WHERE
    pg_namespace.nspname NOT IN ('information_schema', 'catalog_history')
    AND pg_namespace.nspname NOT LIKE 'pg_%'
;