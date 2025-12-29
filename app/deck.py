from dataclasses import dataclass


@dataclass
class Deck:
    row: int
    column: int
    is_alive: bool = True

    def __repr__(self) -> str:
        return f"Deck ({self.row}, {self.column}) alive = {self.is_alive}"
