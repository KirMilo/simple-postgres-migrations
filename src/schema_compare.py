from schema_components.tables import Table
from dataclasses import dataclass


@dataclass
class SchemaChanges:
    new: list[Table]
    changed: list[Table]


class SchemaCompare:
    def __init__(self, target: set[Table], master: set[Table]):
        self.target = target  # образец
        self.master = master  # боевая

    def new_tables(self) -> list[Table]:
        return list(self.target - self.master)

    def tables_difference(self, target: Table, master: Table) -> Table | None:  # NOQA
        target_columns = {column.name: column for column in target.columns}
        master_columns = {column.name: column for column in master.columns}

        changes = []
        for column_name in target_columns:
            if diff := target_columns[column_name] - master_columns.get(column_name):
                changes.append(diff)
        if changes:
            return Table(name=target.name, columns=changes)

        return None

    def changed_tables(self) -> list[Table]:
        target_tables = {table.name: table for table in self.target}
        master_tables = {table.name: table for table in self.master}

        changes = []
        for table_name in master_tables:
            target_table = target_tables.get(table_name)
            master_table = master_tables.get(table_name)
            if not target_table:
                raise Exception('Таблица из боевой БД отсутствует в образце')

            table = self.tables_difference(target_table, master_table)
            if table:
                changes.append(table)

        return changes

    def difference(self) -> SchemaChanges:
        new = self.new_tables()
        changed = self.changed_tables()
        return SchemaChanges(
            new=new,
            changed=changed
        )
