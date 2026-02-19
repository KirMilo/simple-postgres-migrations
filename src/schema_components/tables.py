from dataclasses import dataclass

from .columns import Column, ColumnDiff


@dataclass(eq=False, frozen=True)
class Table:
    name: str
    columns: list[Column | ColumnDiff]
    # TODO: Не учтены constraints

    def __eq__(self, other):
        if not isinstance(other, Table):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
