from dataclasses import dataclass, astuple
from typing import Optional


@dataclass
class Column:
    name: str
    data_type: str
    is_nullable: str  # str не я придумал. В postgre значение char(3) NO или YES
    default_value: str | None = None
    is_primary: bool = False

    def __sub__(self, other: Optional["Column"]) -> Optional["ColumnDiff"]:
        """Возвращает разницу между двумя колонками"""
        if other is None:
            return ColumnDiff(*astuple(self), is_exists=False)
        elif not isinstance(other, Column):
            return NotImplemented

        is_changed = any(
            [
                self.data_type != other.data_type,
                self.is_nullable != other.is_nullable,
                self.default_value != other.default_value,
            ]
        )

        return ColumnDiff(
            *astuple(self),
            is_exists=True,
            type_is_changed=self.data_type != other.data_type,
            is_nullable_is_changed=self.is_nullable != other.is_nullable,
            default_value_is_changed=self.default_value != other.default_value,
        ) if is_changed else None

    def _get_sql_data_type(self):
        data_type = self.data_type
        if self.is_primary:
            if self.data_type == "integer":
                data_type = "SERIAL"
            elif self.data_type == "bigint":
                data_type = "BIGSERIAL"
            data_type += " PRIMARY KEY"

        return data_type

    def create_table_column_sql(self) -> str:
        data_type = self._get_sql_data_type()
        if self.default_value is not None:
            if self.data_type in ("integer", "bigint", "boolean"):
                data_type += f" DEFAULT {self.default_value}"
            else:
                self.data_type += f" DEFAULT '{self.default_value}'"

        if self.is_nullable == "NO":
            data_type += " NOT NULL"

        return f"{self.name} {data_type}"


@dataclass
class ColumnDiff(Column):
    is_exists: bool = True
    type_is_changed: bool = False
    is_nullable_is_changed: bool = False
    default_value_is_changed: bool = False

    def alter_table_column_sql(self) -> str | None:

        if not self.is_exists:
            result = f"ADD COLUMN {self.name} {self.data_type}"
            if self.default_value is not None and self.default_value is not None:

                if self.data_type in ("integer", "bigint", "boolean"):
                    result += f" DEFAULT {self.default_value}"
                else:
                    result += f" DEFAULT '{self.default_value}'"

            if self.is_nullable == "NO":
                result += " NOT NULL"

        elif self.type_is_changed or self.is_nullable_is_changed or self.default_value_is_changed:
            result = f"ALTER COLUMN {self.name} TYPE {self.data_type}"
            if self.type_is_changed:
                raise NotImplementedError('Логика для безопасного изменения типа не реализована')

            if self.default_value_is_changed and self.default_value is not None:

                if self.data_type in ("integer", "bigint", "boolean"):
                    result += f" SET DEFAULT {self.default_value}"
                else:
                    result += f" SET DEFAULT '{self.default_value}'"

            if self.is_nullable_is_changed:
                result += f" SET NOT NULL" if self.is_nullable == "NO" else " DROP NOT NULL"

        else:
            result = None
        return result
