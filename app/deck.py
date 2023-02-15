from app.cell import Cell


class Deck(Cell):
    def __init__(self, cord: tuple) -> None:
        super().__init__(cord)

    def __repr__(self) -> str:
        return "\u25A1"
