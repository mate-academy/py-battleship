from app.cell import Cell


class Carbon(Cell):
    def __init__(self, cord: tuple) -> None:
        super().__init__(cord)

    def __repr__(self) -> str:
        return "*"
