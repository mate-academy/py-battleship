from typing import Any


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    @staticmethod
    def validate_index(data: Any) -> None:
        if not isinstance(data, int):
            raise TypeError("Type should be 'int'")
        if not data >= 0:
            raise ValueError("Value should be >= 0")

    @property
    def row(self) -> int:
        return self._row

    @row.setter
    def row(self, value: int) -> None:
        self.validate_index(value)
        self._row = value

    @property
    def column(self) -> int:
        return self._column

    @column.setter
    def column(self, value: int) -> None:
        self.validate_index(value)
        self._column = value
