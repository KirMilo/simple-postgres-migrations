from psycopg import Connection, sql

from schema_components.columns import Column
from schema_components.tables import Table


QUERY = sql.SQL("""
        SELECT c.table_name,
               json_agg(
                       json_build_object(
                               'column_name', c.column_name,
                               'data_type', c.data_type,
                               'is_nullable', c.is_nullable,
                               'column_default', c.column_default,
                               'is_primary', c.column_name IN (
                                    SELECT kcu.column_name
                                    FROM information_schema.table_constraints tc
                                    JOIN information_schema.key_column_usage kcu
                                        ON tc.constraint_name = kcu.constraint_name
                                    WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.table_name = c.table_name)
                       ) ORDER BY c.ordinal_position
               ) AS columns
        FROM information_schema.columns c
        WHERE c.table_schema = 'public'
        GROUP BY c.table_name
        ORDER BY c.table_name;
""")


class DBSchema:
    def __init__(self, conn: Connection):
        self._conn: Connection = conn

    def _load_schema(self) -> list[tuple[str, list[dict[str, ...]]]]:
        cur = self._conn.cursor()
        cur.execute(QUERY)
        return cur.fetchall()

    def get_tables(self) -> set[Table]:
        tables_columns = self._load_schema()

        tables = set()
        for table_name, columns in tables_columns:
            tables.add(
                Table(
                    name=table_name,
                    columns=[Column(*column_attrs.values()) for column_attrs in columns],
                )
            )
        return tables
