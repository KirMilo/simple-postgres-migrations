from psycopg import Connection
from psycopg.sql import SQL

from schema_components.tables import Table
from schema_compare import SchemaChanges


class Migration:
    def __init__(self, changes: SchemaChanges):
        self.new_tables = changes.new
        self.changed_tables = changes.changed

    def __create_table(self, table: Table) -> str:  # NOQA
        return f"CREATE TABLE {table.name} ({', '.join(
            column.create_table_column_sql() for column in table.columns)
        });"

    def __alter_table(self, table: Table) -> str:  # NOQA
        return f"ALTER TABLE {table.name} {', '.join(
            changes for column in table.columns if (changes := column.alter_table_column_sql()) is not None
        )};"

    def __get_operations(self) -> list[str]:
        operations = []

        for table in self.new_tables:
            operation = self.__create_table(table)
            operations.append(operation)

        for table in self.changed_tables:
            operation = self.__alter_table(table)
            if operation is not None:
                operations.append(operation)

        return operations

    def __generate_sql(self) -> SQL | None:
        operations = self.__get_operations()
        if not operations:
            return None
        return SQL("BEGIN;\n" + "\n".join(operations) + "\nCOMMIT;")

    def apply(self, conn: Connection = None):
        q = self.__generate_sql()
        if not q:
            print("No changes to apply")
        else:
            print(q.as_string())
            if not conn:
                print("Не передано подключения к БД. Изменения не применены")
            else:
                accept = input("\nApply changes? (Y/N): Default: N\n")
                if accept.lower() == "y":
                    conn.execute(q)
                    print("Изменения успешно применены.")
                else:
                    print("Изменения не применены.")